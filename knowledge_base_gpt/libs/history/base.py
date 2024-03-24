""" Base class for history keepers """
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from langchain_core.messages import BaseMessage


class HistoryBase(ABC):
    """ Base class for history keepers """
    @abstractmethod
    def get_messages(self, session_id: str) -> List[BaseMessage]:
        """ Get all messages of the session """

    @abstractmethod
    def add_to_history(self, session_id: str, answer: Dict[str, Any]):
        """ Add the answer to the session """

    @abstractmethod
    def reset(self, session_id: str):
        """ Reset the session """
