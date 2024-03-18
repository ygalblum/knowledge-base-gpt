#!/usr/bin/env python3
from injector import inject, singleton
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from knowledge_base_gpt.libs.injector.di import global_injector
from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.gpt.private_chat import PrivateChat
from knowledge_base_gpt.libs.history.redis import HistoryRedis


class KnowledgeBaseSlackBotException(Exception):
    pass


@singleton
class KnowledgeBaseSlackBot():

    @inject
    def __init__(self, settings: Settings) -> None:
        self.app_token = settings.slackbot.app_token
        self.bot_token = settings.slackbot.bot_token
        self.forward_question_channel_name = settings.slackbot.forward_channel

    def run(self):
        self._app = App(token=self.bot_token)
        self._forward_question_channel_id = self._get_forward_question_channel_id()
        self._app.client.conversations_join(channel=self._forward_question_channel_id)
        self._app.message()(self._got_message)
        self._app.command('/conversation_reset')(self._reset_conversation)
        self._app.command('/conversation_forward')(self._forward_question)
        self._private_chat = PrivateChat()
        SocketModeHandler(self._app, self.app_token).start()

    def _get_forward_question_channel_id(self):
        if self.forward_question_channel_name is None:
            raise KnowledgeBaseSlackBotException(f"FORWARD_QUESTION_CHANNEL_NAME was not set")
        try:
            for result in self._app.client.conversations_list():
                for channel in result["channels"]:
                    if channel["name"] == self.forward_question_channel_name:
                        return channel["id"]
        except SlackApiError as e:
            raise KnowledgeBaseSlackBotException(e)
        raise KnowledgeBaseSlackBotException(f"The channel {self.forward_question_channel_name} does not exits")

    def _got_message(self, message, say):
        self._app.client.chat_postEphemeral(
            channel=message['channel'],
            user=message['user'],
            text="On it. Be back with your answer soon"
        )
        history = HistoryRedis(message['user'])
        answer = self._private_chat.answer_query(history.get_messages(), message['text'], chat_identifier=message['user'])
        history.add_to_history(answer)
        say(answer['answer'])

    def _is_direct_message_channel(self, command):
        if command['channel_name'] == 'directmessage':
            return True
        self._app.client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text='This command can only be triggered on the direct messages channel'
        )
        return False


    def _reset_conversation(self, ack, say, command):
        ack()
        if not self._is_direct_message_channel(command):
            return

        HistoryRedis(command['user_id']).reset()

        self._app.client.chat_postEphemeral(
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

    def _forward_question(self, ack, say, command):
        ack()
        if not self._is_direct_message_channel(command):
            return

        messages = HistoryRedis(command['user_id']).get_messages()
        if len(messages) == 0:
            msg = 'There is no active conversation'
        else:
            self._app.client.chat_postMessage(channel=self._forward_question_channel_id, text=self._messages_to_text(messages))
            msg = f'The conversation was forwarded to {self.forward_question_channel_name}'

        self._app.client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text=msg
        )


def main():
    try:
        global_injector.get(KnowledgeBaseSlackBot).run()
    except KnowledgeBaseSlackBotException as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    main()
