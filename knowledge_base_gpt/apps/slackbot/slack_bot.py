#!/usr/bin/env python3
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from knowledge_base_gpt.libs.gpt.private_chat import PrivateChat
from knowledge_base_gpt.libs.history.redis import HistoryRedis


forward_question_channel_name = os.environ.get("FORWARD_QUESTION_CHANNEL_NAME")


class KnowledgeBaseSlackBotException(Exception):
    pass


class KnowledgeBaseSlackBot():
    __instance = None

    @staticmethod
    def get_instance():
        if KnowledgeBaseSlackBot.__instance is None:
            KnowledgeBaseSlackBot()
        return KnowledgeBaseSlackBot.__instance

    def __init__(self):
        if KnowledgeBaseSlackBot.__instance is not None:
            raise KnowledgeBaseSlackBotException("This class is a singleton!")
        KnowledgeBaseSlackBot.__instance = self

    def run(self):
        self._app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
        self._forward_question_channel_id = self._get_forward_question_channel_id()
        self._app.client.conversations_join(channel=self._forward_question_channel_id)
        self._app.message()(KnowledgeBaseSlackBot.got_message)
        self._app.command('/conversation_reset')(KnowledgeBaseSlackBot.reset_conversation)
        self._app.command('/conversation_forward')(KnowledgeBaseSlackBot.forward_question)
        self._private_chat = PrivateChat()
        SocketModeHandler(self._app, os.environ["SLACK_APP_TOKEN"]).start()

    def _get_forward_question_channel_id(self):
        if forward_question_channel_name is None:
            raise KnowledgeBaseSlackBotException(f"FORWARD_QUESTION_CHANNEL_NAME was not set")
        try:
            for result in self._app.client.conversations_list():
                for channel in result["channels"]:
                    if channel["name"] == forward_question_channel_name:
                        return channel["id"]
        except SlackApiError as e:
            raise KnowledgeBaseSlackBotException(e)
        raise KnowledgeBaseSlackBotException(f"The channel {forward_question_channel_name} does not exits")

    def _got_message(self, message, say):
        self._app.client.chat_postEphemeral(
            channel=message['channel'],
            user=message['user'],
            text="On it. Be back with your answer soon"
        )
        history = HistoryRedis(message['user'])
        answer = self._private_chat.answer_query(history.get_messages(), message['text'])
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
            msg = f'The conversation was forwarded to {forward_question_channel_name}'

        self._app.client.chat_postEphemeral(
            channel=command['channel_id'],
            user=command['user_id'],
            text=msg
        )

    @staticmethod
    def got_message(message, say):
        return KnowledgeBaseSlackBot.get_instance()._got_message(message, say)

    @staticmethod
    def reset_conversation(ack, say, command):
        return KnowledgeBaseSlackBot.get_instance()._reset_conversation(ack, say, command)

    @staticmethod
    def forward_question(ack, say, command):
        return KnowledgeBaseSlackBot.get_instance()._forward_question(ack, say, command)


def main():
    try:
        KnowledgeBaseSlackBot.get_instance().run()
    except KnowledgeBaseSlackBotException as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    main()
