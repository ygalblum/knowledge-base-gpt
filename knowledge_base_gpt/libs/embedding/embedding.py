""" Create and abstract the embedding """
from injector import inject, singleton
from langchain_core.embeddings import Embeddings as LangChainEmbeddings

from knowledge_base_gpt.libs.logs.logger import ApplicationLogger
from knowledge_base_gpt.libs.settings.settings import Settings


@singleton
class Embedding():  # pylint:disable=R0903,C0415
    """ Create and abstract the embedding """
    @inject
    def __init__(self, settings: Settings, application_logger: ApplicationLogger) -> None:
        mode = settings.embedding.mode
        match mode:
            case 'hugging_face':
                from langchain_huggingface import HuggingFaceEmbeddings

                application_logger.logger.info("Using Hugging Face Embeddings")
                self._embeddings = HuggingFaceEmbeddings(model_name=settings.hugging_face.embedding_model)
            case 'ollama':
                from langchain_community.embeddings import OllamaEmbeddings

                ollama_settings = settings.ollama
                application_logger.logger.info("Using Ollama Embeddings")
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
            case 'infinity':
                from langchain_community.embeddings import InfinityEmbeddings

                infinity_settings = settings.infinity
                application_logger.logger.info("Using Inifinity Embeddings")
                self._embeddings = InfinityEmbeddings(
                    model=infinity_settings.embedding_model,
                    infinity_api_url=infinity_settings.api_url
                )
            case 'fake':
                from langchain_core.embeddings.fake import FakeEmbeddings

                self._embeddings = FakeEmbeddings(size=128)
            case _:
                pass

    @property
    def embeddings(self) -> LangChainEmbeddings:
        """ Return the embedding implementation """
        return self._embeddings
