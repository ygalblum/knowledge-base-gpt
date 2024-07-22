""" Manage Application logs """
import logging
from logging.handlers import RotatingFileHandler
import sys

from injector import inject, singleton

from knowledge_base_gpt.libs.settings.settings import Settings


@singleton
class ApplicationLogger():  # pylint:disable=R0903
    """ Application Logger """

    @inject
    def __init__(self, settings: Settings):
        if settings.log.application_log_path:
            handler = RotatingFileHandler(
                settings.log.chat_log_path,
                maxBytes=settings.log.chat_log_max_bytes,
                backupCount=settings.log.chat_log_backup_count
            )
        else:
            handler = logging.StreamHandler(sys.stdout)

        handler.setLevel(logging.getLevelNamesMapping()[settings.log.application_log_level])
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self._logger = logging.getLogger("application_log")
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(handler)

    @property
    def logger(self) -> logging.Logger:
        """ Get the python logger """
        return self._logger
