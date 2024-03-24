""" Manage history in Redis """
from typing import List, Dict, Any

from injector import inject, singleton
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import BaseMessage

from knowledge_base_gpt.libs.history.base import HistoryBase
from knowledge_base_gpt.libs.settings.settings import RedisSettings, Settings


@singleton
class HistoryRedis(HistoryBase):
    """ Manage history in Redis """
    @inject
    def __init__(self, settings: Settings):
        redis_settings = settings.redis
        self._url = self._build_url_string(redis_settings)
        self._ttl = redis_settings.ttl

    def get_messages(self, session_id: str) -> List[BaseMessage]:
        return RedisChatMessageHistory(session_id, url=self._url, ttl=self._ttl).messages

    def add_to_history(self, session_id: str, answer: Dict[str, Any]):
        h = RedisChatMessageHistory(session_id, url=self._url, ttl=self._ttl)
        h.add_user_message(answer['question'])
        h.add_ai_message(answer['answer'])

    def reset(self, session_id: str):
        RedisChatMessageHistory(session_id, url=self._url, ttl=self._ttl).clear()

    @staticmethod
    def _build_url_string(redis_settings: RedisSettings):
        url = "redis://"
        if redis_settings.username or redis_settings.password:
            username = redis_settings.username if redis_settings.username else ''
            password = redis_settings.password if redis_settings.password else ''
            url += f"{username}:{password}@"
        url += f"{redis_settings.host}:6379/0"
        return url
