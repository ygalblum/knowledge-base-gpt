import os

from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma

from knowledge_base_gpt.libs.common import constants
from knowledge_base_gpt.libs.logs.ollama import OllamaChatFragment, OllamaChatLogExporter
from knowledge_base_gpt.libs.gpt.ollama_info import get_ollama_callback

model = os.environ.get("MODEL", "llama2-uncensored")
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))
ollama_host = os.environ.get("OLLAMA_HOST", 'localhost')
ollama_port = os.environ.get("OLLAMA_PORT", '11434')
chat_logs_file = os.environ.get("CHAT_LOGS_FILE", "/var/log/chatlogs.log")


class PrivateChat():

    def __init__(self, verbose=False):
        self._logs_exporter = OllamaChatLogExporter(chat_logs_file)
        embeddings = HuggingFaceEmbeddings(model_name=constants.embeddings_model_name)
        db = Chroma(persist_directory=constants.persist_directory, embedding_function=embeddings)
        retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
        chat = ChatOllama(model=model, base_url=f"http://{ollama_host}:{ollama_port}")
        self._chain = ConversationalRetrievalChain.from_llm(
            llm=chat,
            retriever=retriever,
            verbose=verbose,
            return_source_documents=True,
            return_generated_question=True
        )

    def answer_query(self, history, query, chat_identifier=None):
        with get_ollama_callback() as cb:
            answer = self._chain({"question": query, "chat_history": history})
            self._logs_exporter.save_chat_log(OllamaChatFragment(answer, cb, chat_identifier=chat_identifier))
            return answer
