import json

from injector import inject, singleton

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.logs.chat_fragment import ChatFragment


@singleton
class ChatLogExporter():

    @inject
    def __init__(self, settings: Settings):
        self._path = settings.log.chat_log_path

    def save_chat_log(self, chat_fragment: ChatFragment):
        with open(self._path, "a+") as f:
            f.write(f"{json.dumps(chat_fragment.to_json())}\n")
