""" Manage history in Memory """
from typing import List, Dict, Any, Union

from langchain_core.messages import BaseMessage, AIMessage, HumanMessage

from knowledge_base_gpt.libs.history.base import HistoryBase


class HistoryMemory(HistoryBase):
    """ Manage history in memory """
    def __init__(self):
        self._messages: Dict[str, List[BaseMessage]] = {}
        self._chat_identifiers: Dict[str, str] = {}

    def get_messages(self, session_id: str) -> List[BaseMessage]:
        return self._messages.get(session_id, [])

    def add_to_history(self, session_id: str, answer: Dict[str, Any]):
        if self._messages.get(session_id) is None:
            self._messages[session_id] = []
        self._messages[session_id].extend(
            [
                self._get_human_message(answer['question']),
                self._get_ai_message(answer['answer'])
            ]

        )

    def reset(self, session_id: str):
        if self._messages.get(session_id) is not None:
            del self._messages[session_id]

    @staticmethod
    def _get_human_message(message: Union[HumanMessage, str]) -> HumanMessage:
        if not isinstance(message, HumanMessage):
            message = HumanMessage(content=message)
        return message

    @staticmethod
    def _get_ai_message(message: Union[AIMessage, str]) -> AIMessage:
        if not isinstance(message, AIMessage):
            message = AIMessage(content=message)
        return message

    def _fetch_chat_identifier(self, user_id: str) -> Union[str, None]:
        return self._chat_identifiers.get(user_id)

    def _store_chat_identifier(self, user_id: str, chat_identifier: str):
        self._chat_identifiers[user_id] = chat_identifier
