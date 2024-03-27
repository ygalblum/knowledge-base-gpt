""" Manage history """
from injector import inject, singleton

from knowledge_base_gpt.libs.history.base import HistoryBase
from knowledge_base_gpt.libs.history.redis import HistoryRedis
from knowledge_base_gpt.libs.history.memory import HistoryMemory
from knowledge_base_gpt.libs.settings.settings import Settings


@singleton
class History():  # pylint:disable=R0903
    """ Wrap history manager based on settings """
    @inject
    def __init__(self, settings: Settings) -> None:
        match settings.history.mode:
            case 'memory':
                self._history = HistoryMemory()
            case 'redis':
                self._history = HistoryRedis(settings.redis)
            case _:
                pass

    @property
    def history(self) -> HistoryBase:
        """ Get history manager """
        return self._history
