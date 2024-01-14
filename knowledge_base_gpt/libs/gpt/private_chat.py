import os

from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma

from knowledge_base_gpt.libs.common import constants

model = os.environ.get("MODEL", "llama2-uncensored")
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))
ollama_host = os.environ.get("OLLAMA_HOST", 'localhost')
redis_host = os.environ.get("REDIS_HOST", 'localhost')


class PrivateChat():

    def __init__(self, hide_source=True, verbose=False):
        embeddings = HuggingFaceEmbeddings(model_name=constants.embeddings_model_name)
        db = Chroma(persist_directory=constants.persist_directory, embedding_function=embeddings)
        retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
        chat = ChatOllama(model=model, base_url=f"http://{ollama_host}:11434")
        self._chain = ConversationalRetrievalChain.from_llm(
            llm=chat,
            retriever=retriever,
            verbose=verbose,
            return_source_documents=hide_source,
        )

    def answer_query(self, session_id, query):
        history = RedisChatMessageHistory(session_id, url=f"redis://{redis_host}:6379/0", ttl=3000)
        answer = self._chain({"question": query, "chat_history": history.messages})
        history.add_user_message(answer['question'])
        history.add_ai_message(answer['answer'])
        return answer['answer']

    @staticmethod
    def reset_conversation(session_id):
        RedisChatMessageHistory(session_id, url=f"redis://{redis_host}:6379/0", ttl=3000).clear()

    @staticmethod
    def get_conversation(session_id):
        return RedisChatMessageHistory(session_id, url=f"redis://{redis_host}:6379/0", ttl=3000).messages
