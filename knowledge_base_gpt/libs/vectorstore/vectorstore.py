from chromadb.config import Settings as ChromaSettings
from injector import inject, singleton
from langchain_community.vectorstores.chroma import Chroma


from knowledge_base_gpt.libs.embedding.embedding import Embedding
from knowledge_base_gpt.libs.settings.settings import Settings


@singleton
class VectorStore():
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
        return self._db
