""" Export Chat logs to File """
import json
import logging
from logging.handlers import RotatingFileHandler

from injector import inject, singleton

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.logs.chat_fragment import ChatFragment


@singleton
class ChatLogExporter():  # pylint:disable=R0903
    """ Export Chat logs to File """

    @inject
    def __init__(self, settings: Settings):
        self._chat_log_enabled = settings.log.chat_log_enabled
        if not self._chat_log_enabled:
            return
        handler = RotatingFileHandler(
            settings.log.chat_log_path,
            maxBytes=settings.log.chat_log_max_bytes,
            backupCount=settings.log.chat_log_backup_count)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self._logger = logging.getLogger("chatlog")
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(handler)

    def save_chat_log(self, chat_fragment: ChatFragment):
        """ Save the Chat log fragment to the log file """
        if self._chat_log_enabled:
            self._logger.info(json.dumps(chat_fragment.to_json()))
