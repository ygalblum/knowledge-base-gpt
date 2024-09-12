""" Slackbot application backend """
from typing import Any

from injector import inject, singleton
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
from slack_sdk.web import WebClient

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.gpt.private_chat import PrivateChat
from knowledge_base_gpt.libs.history.history import History
from knowledge_base_gpt.libs.logs.logger import ApplicationLogger


class KnowledgeBaseSlackBotException(Exception):
    """ Wrapper for SlackBot specific exception """


@singleton
class KnowledgeBaseSlackBot():  # pylint:disable=R0903
    """ Slackbot application backend """

    @inject
    def __init__(
        self,
        settings: Settings,
        private_chat: PrivateChat,
        history: History,
        application_logger: ApplicationLogger
    ) -> None:
        # Store references to other singletons
        self._private_chat = private_chat
        self._history = history
        self._logger = application_logger.logger

        # Create the socket mode handler
        client_params: dict[str, Any] = {"token": settings.slackbot.bot_token}
        # Override Base URL for testing against a mock server
        if settings.slackbot.base_url:
            client_params['base_url'] = settings.slackbot.base_url
        client = WebClient(**client_params)

        # Add the RateLimit Error Retry Handler
        client.retry_handlers.append(RateLimitErrorRetryHandler(max_retry_count=5))

        self._handler = SocketModeHandler(
            app=App(client=client),
            app_token=settings.slackbot.app_token
        )

        # Handle forward channel
        self._forward_question_channel_name = settings.slackbot.forward_channel
        self._forward_question_channel_id = self._get_forward_question_channel_id()
        self._handler.app.client.conversations_join(channel=self._forward_question_channel_id)

        # Register message and command handlers
        self._handler.app.message()(self._got_message)

        cmd_string = f'/{settings.slackbot.command_strings.reset}'
        self._logger.info("Registering to %s as reset command", cmd_string)
        self._handler.app.command(cmd_string)(self._reset_conversation)

        cmd_string = f'/{settings.slackbot.command_strings.forward}'
        self._logger.info("Registering to %s as forward command", cmd_string)
        self._handler.app.command(cmd_string)(self._forward_question)

    def run(self):
        """ Start the Slackbot backend application """
        self._logger.info("Connecting to the Slack Server")
        self._handler.start()

    def _get_forward_question_channel_id(self):
        if self._forward_question_channel_name is None:
            raise KnowledgeBaseSlackBotException("Slackbot forward channel name was not set")
        try:
            for result in self._handler.app.client.conversations_list():
                for channel in result["channels"]:
                    if channel["name"] == self._forward_question_channel_name:
                        return channel["id"]
        except SlackApiError as e:
            raise KnowledgeBaseSlackBotException(e) from e
        raise KnowledgeBaseSlackBotException(f"The channel {self._forward_question_channel_name} does not exits")

    def _got_message(self, message, say):
        self._logger.debug("Got a new message")
        self._handler.app.client.chat_postEphemeral(
            channel=message['channel'],
            user=message['user'],
            text="On it. Be back with your answer soon"
        )
        session_id = self._history.history.get_chat_identifier(message['user'])
        try:
            answer = self._private_chat.answer_query(
                self._history.history.get_messages(session_id),
                message['text'],
                chat_identifier=session_id
            )
        except Exception as e:  # pylint:disable=W0718
            self._logger.error("Failed to answer the query", e)
            self._handler.app.client.chat_postEphemeral(
                channel=message['channel'],
                user=message['user'],
                text="I have encountered an error. Please try again later"
            )
        else:
            self._history.history.add_to_history(session_id, answer)
            say(answer['answer'])

    def _is_direct_message_channel(self, command):
        if command['channel_name'] == 'directmessage':
            return True
        self._handler.app.client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text='This command can only be triggered on the direct messages channel'
        )
        return False

    def _reset_conversation(self, ack, say, command):  # pylint:disable=unused-argument
        ack()
        if not self._is_direct_message_channel(command):
            return

        self._logger.debug("Resetting the conversation")
        self._history.history.reset(self._history.history.get_chat_identifier(command['user_id']))

        self._handler.app.client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text='The previous conversation was cleared. You can start a new one now'
        )

    @staticmethod
    def _messages_to_text(messages):
        text = ''
        for message in messages:
            text += "Question: " if message.type == 'human' else "Answer: "
            text += message.content
            text += '\n'
        return text

    def _forward_question(self, ack, say, command):  # pylint:disable=unused-argument
        ack()
        if not self._is_direct_message_channel(command):
            return

        messages = self._history.history.get_messages(self._history.history.get_chat_identifier(command['user_id']))
        if len(messages) == 0:
            msg = 'There is no active conversation'
        else:
            # Do not log the channel name
            self._logger.debug("Forwarding the conversion to the predefined channel")
            self._handler.app.client.chat_postMessage(
                channel=self._forward_question_channel_id,
                text=self._messages_to_text(messages)
            )
            msg = f'The conversation was forwarded to {self._forward_question_channel_name}'

        self._handler.app.client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text=msg
        )
