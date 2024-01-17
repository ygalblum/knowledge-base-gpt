from abc import ABC, abstractmethod
from typing import List

from langchain_core.messages import BaseMessage


class HistoryBase(ABC):
    @abstractmethod
    def get_messages(self) -> List[BaseMessage]:
        pass

    @abstractmethod
    def add_to_history(self, answer):
        pass

    @abstractmethod
    def reset(self):
        pass
