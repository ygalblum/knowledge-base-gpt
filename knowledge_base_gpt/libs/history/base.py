""" Base class for history keepers """
from abc import ABC, abstractmethod
import uuid
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

    def get_chat_identifier(self, user_id: str) -> str:
        """ Get (or create) the chat identifier linked to the user_id. """
        chat_identifier = self._fetch_chat_identifier(user_id)
        if not chat_identifier:
            chat_identifier = str(uuid.uuid4())
            self._store_chat_identifier(user_id, chat_identifier)
        return chat_identifier

    @abstractmethod
    def _fetch_chat_identifier(self, user_id: str) -> str:
        """ Get the chat identifier from the history """

    @abstractmethod
    def _store_chat_identifier(self, user_id: str, chat_identifier: str):
        """ Store the chat identifier in the history """
