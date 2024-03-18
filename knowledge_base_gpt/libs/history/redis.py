import os
from typing import List

from injector import inject, singleton
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import BaseMessage

from knowledge_base_gpt.libs.history.base import HistoryBase
from knowledge_base_gpt.libs.settings.settings import Settings


@singleton
class HistoryRedis(HistoryBase):

    @inject
    def __init__(self, settings: Settings):
        redis_settings = settings.redis
        self._url = f"redis://{':' + redis_settings.password + '@' if redis_settings.password else '' }{redis_settings.host}:6379/0"
        self._ttl = redis_settings.ttl

    def get_messages(self, session_id) -> List[BaseMessage]:
        return RedisChatMessageHistory(session_id, url=self._url, ttl=self._ttl).messages

    def add_to_history(self, session_id, answer):
        h = RedisChatMessageHistory(session_id, url=self._url, ttl=self._ttl)
        h.add_user_message(answer['question'])
        h.add_ai_message(answer['answer'])

    def reset(self, session_id: str):
        RedisChatMessageHistory(session_id, url=self._url, ttl=self._ttl).clear()
