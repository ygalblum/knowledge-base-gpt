""" Manage history in Redis """
from typing import List, Dict, Any, Union

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_community.utilities.redis import get_client
from langchain_core.messages import BaseMessage

from knowledge_base_gpt.libs.history.base import HistoryBase
from knowledge_base_gpt.libs.settings.settings import RedisSettings


class HistoryRedis(HistoryBase):
    """ Manage history in Redis """
    def __init__(self, redis_settings: RedisSettings):
        self._url = self._build_url_string(redis_settings)
        self._ttl = redis_settings.ttl
        self._chat_identifier_key_prefix = redis_settings.chat_identifier_key_prefix
        self._client = get_client(self._url)

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

    def _chat_identifier_key(self, user_id: str) -> str:
        return f"{self._chat_identifier_key_prefix}{user_id}"

    def _fetch_chat_identifier(self, user_id: str) -> Union[str, None]:
        v = self._client.get(self._chat_identifier_key(user_id))
        if v is None:
            return None
        return bytes(v).decode("utf-8")

    def _store_chat_identifier(self, user_id: str, chat_identifier: str):
        self._client.set(self._chat_identifier_key(user_id), chat_identifier)
