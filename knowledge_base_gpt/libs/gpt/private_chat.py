from typing import Optional

from injector import inject, singleton
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.logs.chat_log_exporter import ChatLogExporter
from knowledge_base_gpt.libs.logs.ollama import OllamaChatFragment
from knowledge_base_gpt.libs.gpt.ollama_info import get_ollama_callback
from knowledge_base_gpt.libs.vectorstore.vectorstore import VectorStore


@singleton
class PrivateChat():

    @inject
    def __init__(self, settings: Settings, chat_log_exporter: ChatLogExporter, vector_store: VectorStore):
        llm_mode = settings.llm.mode
        match llm_mode:
            case 'ollama':
                ollama_settings = settings.ollama
                self._chat_log_exporter = chat_log_exporter
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
            case 'mock':
                pass
            case _:
                pass
        self._chain = ConversationalRetrievalChain.from_llm(
            llm=chat,
            retriever=vector_store.db.as_retriever(search_kwargs={"k": settings.llm.num_documents}),
            verbose=settings.llm.verbose,
            return_source_documents=True,
            return_generated_question=True
        )

    def answer_query(self, history, query, chat_identifier: Optional[str]=None):
        with self._get_callback() as cb:
            answer = self._chain.invoke({"question": query, "chat_history": history})
            self._chat_log_exporter.save_chat_log(self._chat_fragment_cls(answer, cb, chat_identifier=chat_identifier))
            return answer
