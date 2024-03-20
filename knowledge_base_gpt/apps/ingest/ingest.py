import os
from typing import List

from injector import inject, singleton
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.loaders.loaders import Loader
from knowledge_base_gpt.libs.vectorstore.vectorstore import VectorStore


@singleton
class Ingestor():

    @inject
    def __init__(self, settings: Settings, loader: Loader, vector_store: VectorStore) -> None:
        self._loader = loader
        self._chunk_size = settings.text_splitter.chunk_size
        self._chunk_overlap = settings.text_splitter.chunk_overlap
        self._vector_store = vector_store

    def _process_documents(self, ignored_files: List[str] = []) -> List[Document]:
        """
        Load documents and split in chunks
        """
        print(f"Loading documents")
        documents = self._loader.load_documents(ignored_files)
        if not documents:
            return []

        print(f"Loaded {len(documents)} new documents")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self._chunk_size, chunk_overlap=self._chunk_overlap)
        documents = text_splitter.split_documents(documents)
        print(f"Split into {len(documents)} chunks of text (max. {self._chunk_size} tokens each)")
        return documents

    def run(self):
        collection = self._vector_store.db.get()
        documents = self._process_documents(list(set(metadata['source'] for metadata in collection['metadatas'])))
        if len(documents) == 0:
            print("No new documents to load")
        else:
            print(f"Creating embeddings. May take some minutes...")
            self._vector_store.db.add_documents(documents)
            self._vector_store.db.persist()
        print(f"Ingestion complete! You can now run privateGPT.py to query your documents")
