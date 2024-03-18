from abc import ABC, abstractmethod
from typing import List

from langchain_core.messages import BaseMessage


class HistoryBase(ABC):
    @abstractmethod
    def get_messages(self, session_id) -> List[BaseMessage]:
        pass

    @abstractmethod
    def add_to_history(self, session_id, answer):
        pass

    @abstractmethod
    def reset(self, session_id):
        pass
