import os
from typing import List

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import BaseMessage

from knowledge_base_gpt.libs.history.base import HistoryBase

redis_host = os.environ.get("REDIS_HOST", 'localhost')


class HistoryRedis(HistoryBase):

    def __init__(self, session_id):
        self._history = RedisChatMessageHistory(session_id, url=f"redis://{redis_host}:6379/0", ttl=3000)

    def get_messages(self) -> List[BaseMessage]:
        return self._history.messages

    def add_to_history(self, answer):
        self._history.add_user_message(answer['question'])
        self._history.add_ai_message(answer['answer'])

    def reset(self):
        self._history.clear()
