""" Export Chat logs to File """
import json

from injector import inject, singleton

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.logs.chat_fragment import ChatFragment


@singleton
class ChatLogExporter():  # pylint:disable=R0903
    """ Export Chat logs to File """

    @inject
    def __init__(self, settings: Settings):
        self._chat_log_enabled = settings.log.chat_log_enabled
        self._chat_log_path = settings.log.chat_log_path

    def save_chat_log(self, chat_fragment: ChatFragment):
        """ Save the Chat log fragment to the log file """
        if self._chat_log_enabled:
            with open(self._chat_log_path, "a+", encoding="utf-8") as f:
                f.write(f"{json.dumps(chat_fragment.to_json())}\n")
