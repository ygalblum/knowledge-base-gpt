""" Slackbot application backend """
from injector import inject, singleton
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.gpt.private_chat import PrivateChat
from knowledge_base_gpt.libs.history.history import History


class KnowledgeBaseSlackBotException(Exception):
    """ Wrapper for SlackBot specific exception """


@singleton
class KnowledgeBaseSlackBot():  # pylint:disable=R0903
    """ Slackbot application backend """

    @inject
    def __init__(self, settings: Settings, private_chat: PrivateChat, history: History) -> None:
        self._private_chat = private_chat
        self._history = history
        self._handler = SocketModeHandler(App(token=settings.slackbot.bot_token), settings.slackbot.app_token)
        self._forward_question_channel_name = settings.slackbot.forward_channel
        self._forward_question_channel_id = self._get_forward_question_channel_id()
        self._handler.app.client.conversations_join(channel=self._forward_question_channel_id)
        self._handler.app.message()(self._got_message)
        self._handler.app.command('/conversation_reset')(self._reset_conversation)
        self._handler.app.command('/conversation_forward')(self._forward_question)

    def run(self):
        """ Start the Slackbot backend application """
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
        except:  # pylint:disable=W0702
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
