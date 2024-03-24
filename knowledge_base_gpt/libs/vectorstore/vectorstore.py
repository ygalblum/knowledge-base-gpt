""" Module to create and abstract the actual vector store based on the configuration """
from injector import inject, singleton
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores.chroma import Chroma

from knowledge_base_gpt.libs.embedding.embedding import Embedding
from knowledge_base_gpt.libs.settings.settings import Settings


@singleton
class VectorStore():  # pylint:disable=R0903
    """ Abstract the actual vector store based on the configuration """
    @inject
    def __init__(self, settings: Settings, embedding: Embedding) -> None:
        mode = settings.vectorstore.mode
        match mode:
            case 'chroma':
                self._db = Chroma(
                    persist_directory=settings.vectorstore.persist_directory,
                    embedding_function=embedding.embeddings,
                    client_settings=ChromaSettings(
                        is_persistent=True,
                        persist_directory=settings.vectorstore.persist_directory,
                        anonymized_telemetry=False
                    )
                )
            case 'mock':
                pass
            case _:
                pass

    @property
    def db(self):
        """ Return the Vector Store implementation """
        return self._db
