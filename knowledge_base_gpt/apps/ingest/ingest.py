import os
from typing import List

from injector import inject, singleton

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from knowledge_base_gpt.libs.common import constants
from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.loaders.loaders import Loader


@singleton
class Ingestor():

    @inject
    def __init__(self, settings: Settings, loader: Loader) -> None:
        self._loader = loader
        self._chunk_size = settings.text_splitter.chunk_size
        self._chunk_overlap = settings.text_splitter.chunk_overlap

    def _process_documents(self, ignored_files: List[str] = []) -> List[Document]:
        """
        Load documents and split in chunks
        """
        print(f"Loading documents")
        documents = self._loader.load_documents(ignored_files)
        if not documents:
            print("No new documents to load")
            exit(0)
        print(f"Loaded {len(documents)} new documents")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self._chunk_size, chunk_overlap=self._chunk_overlap)
        texts = text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} chunks of text (max. {self._chunk_size} tokens each)")
        return texts

    @staticmethod
    def _does_vectorstore_exist(persist_directory: str) -> bool:
        """
        Checks if vectorstore exists
        """
        return os.path.exists(os.path.join(persist_directory, 'chroma.sqlite3'))

    def run(self):
        # Create embeddings
        embeddings = HuggingFaceEmbeddings(model_name=constants.embeddings_model_name)

        if self._does_vectorstore_exist(constants.persist_directory):
            # Update and store locally vectorstore
            print(f"Appending to existing vectorstore at {constants.persist_directory}")
            db = Chroma(persist_directory=constants.persist_directory, embedding_function=embeddings, client_settings=constants.CHROMA_SETTINGS)
            collection = db.get()
            texts = self._process_documents(list(set(metadata['source'] for metadata in collection['metadatas'])))
            print(f"Creating embeddings. May take some minutes...")
            db.add_documents(texts)
        else:
            # Create and store locally vectorstore
            print("Creating new vectorstore")
            texts = self._process_documents()
            print(f"Creating embeddings. May take some minutes...")
            db = Chroma.from_documents(texts, embeddings, persist_directory=constants.persist_directory)
        db.persist()
        db = None

        print(f"Ingestion complete! You can now run privateGPT.py to query your documents")
