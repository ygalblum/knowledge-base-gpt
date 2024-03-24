""" Create and abstract the embedding """
from injector import inject, singleton
from langchain_core.embeddings import Embeddings as LangChainEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings, OllamaEmbeddings

from knowledge_base_gpt.libs.settings.settings import Settings


@singleton
class Embedding():  # pylint:disable=R0903
    """ Create and abstract the embedding """
    @inject
    def __init__(self, settings: Settings) -> None:
        mode = settings.embedding.mode
        match mode:
            case 'hugging_face':
                self._embeddings = HuggingFaceEmbeddings(model_name=settings.hugging_face.embedding_model)
            case 'ollama':
                ollama_settings = settings.ollama
                self._embeddings = OllamaEmbeddings(
                    model=ollama_settings.embedding_model,
                    base_url=ollama_settings.api_base,
                    temperature=settings.embedding.temperature,
                    tfs_z=ollama_settings.tfs_z,
                    top_k=ollama_settings.top_k,
                    top_p=ollama_settings.top_p,
                    repeat_last_n=ollama_settings.repeat_last_n,
                    repeat_penalty=ollama_settings.repeat_penalty,
                )
            case 'mock':
                pass
            case _:
                pass

    @property
    def embeddings(self) -> LangChainEmbeddings:
        """ Return the embedding implementation """
        return self._embeddings
