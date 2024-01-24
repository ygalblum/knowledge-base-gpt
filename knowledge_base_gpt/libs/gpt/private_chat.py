import os

from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma

from knowledge_base_gpt.libs.common import constants

model = os.environ.get("MODEL", "llama2-uncensored")
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))
ollama_host = os.environ.get("OLLAMA_HOST", 'localhost')
ollama_port = os.environ.get("OLLAMA_PORT", '11434')


class PrivateChat():

    def __init__(self, hide_source=True, verbose=False):
        embeddings = HuggingFaceEmbeddings(model_name=constants.embeddings_model_name)
        db = Chroma(persist_directory=constants.persist_directory, embedding_function=embeddings)
        retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
        chat = ChatOllama(model=model, base_url=f"http://{ollama_host}:{ollama_port}")
        self._chain = ConversationalRetrievalChain.from_llm(
            llm=chat,
            retriever=retriever,
            verbose=verbose,
            return_source_documents=hide_source,
        )

    def answer_query(self, history, query):
        return self._chain({"question": query, "chat_history": history})
