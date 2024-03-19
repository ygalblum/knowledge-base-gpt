import os

from injector import inject, singleton
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.common import constants
from knowledge_base_gpt.libs.logs.ollama import OllamaChatFragment, OllamaChatLogExporter
from knowledge_base_gpt.libs.gpt.ollama_info import get_ollama_callback

target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))
chat_logs_file = os.environ.get("CHAT_LOGS_FILE", "/var/log/chatlogs.log")


@singleton
class PrivateChat():

    @inject
    def __init__(self, settings: Settings):
        llm_mode = settings.llm.mode
        match llm_mode:
            case 'ollama':
                ollama_settings = settings.ollama
                self._logs_exporter = OllamaChatLogExporter(chat_logs_file)
                embeddings = HuggingFaceEmbeddings(model_name=constants.embeddings_model_name)
                db = Chroma(persist_directory=constants.persist_directory, embedding_function=embeddings)
                retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
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
                self._chain = ConversationalRetrievalChain.from_llm(
                    llm=chat,
                    retriever=retriever,
                    verbose=settings.ollama.verbose,
                    return_source_documents=True,
                    return_generated_question=True
                )
            case 'mock':
                pass
            case _:
                pass

    def answer_query(self, history, query, chat_identifier=None):
        with get_ollama_callback() as cb:
            answer = self._chain.invoke({"question": query, "chat_history": history})
            self._logs_exporter.save_chat_log(OllamaChatFragment(answer, cb, chat_identifier=chat_identifier))
            return answer
