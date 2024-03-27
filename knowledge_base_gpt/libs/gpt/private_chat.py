"""
Module for handling the chat chain
"""
from contextlib import nullcontext
import json
from typing import Optional, Dict, Any, List

from injector import inject, singleton
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama, FakeListChatModel

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.logs.chat_log_exporter import ChatLogExporter
from knowledge_base_gpt.libs.logs.ollama import OllamaChatFragment
from knowledge_base_gpt.libs.logs.fake import FakeChatFragment
from knowledge_base_gpt.libs.gpt.ollama_info import get_ollama_callback
from knowledge_base_gpt.libs.vectorstore.vectorstore import VectorStore


@singleton
class PrivateChat():  # pylint:disable=R0903
    """ Handle the Chat chain """
    @inject
    def __init__(self, settings: Settings, chat_log_exporter: ChatLogExporter, vector_store: VectorStore):
        llm_mode = settings.llm.mode
        match llm_mode:
            case 'ollama':
                ollama_settings = settings.ollama
                chat = ChatOllama(
                    model=ollama_settings.llm_model,
                    base_url=ollama_settings.api_base,
                    temperature=settings.llm.temperature,
                    tfs_z=ollama_settings.tfs_z,
                    num_predict=ollama_settings.num_predict,
                    top_k=ollama_settings.top_k,
                    top_p=ollama_settings.top_p,
                    repeat_last_n=ollama_settings.repeat_last_n,
                    repeat_penalty=ollama_settings.repeat_penalty,
                )
                self._get_callback = get_ollama_callback
                self._chat_fragment_cls = OllamaChatFragment
            case 'fake':
                chat = FakeListChatModel(responses=self._load_fake_responses(settings.fake_model.response_path))
                self._get_callback = nullcontext
                self._chat_fragment_cls = FakeChatFragment
            case _:
                pass
        self._chat_log_exporter = chat_log_exporter
        self._chain = ConversationalRetrievalChain.from_llm(
            llm=chat,
            retriever=vector_store.db.as_retriever(search_kwargs={"k": settings.llm.num_documents}),
            verbose=settings.llm.verbose,
            return_source_documents=True,
            return_generated_question=True
        )

    @staticmethod
    def _load_fake_responses(path: str) -> List[str]:
        with open(path, "r", encoding="utf-8") as fd:
            return json.load(fd)

    def answer_query(self, history, query, chat_identifier: Optional[str] = None) -> Dict[str, Any]:
        """
         Answer the query based on the history
         Use the chat identifier for logging the chat
        """
        with self._get_callback() as cb:
            answer = self._chain.invoke({"question": query, "chat_history": history})
            self._chat_log_exporter.save_chat_log(self._chat_fragment_cls(answer, cb, chat_identifier=chat_identifier))
            return answer
