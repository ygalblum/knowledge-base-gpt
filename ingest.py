#!/usr/bin/env python3
import os
import glob
from typing import List

from langchain.document_loaders import GoogleDriveLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from constants import CHROMA_SETTINGS


# Load environment variables
persist_directory = os.environ.get('PERSIST_DIRECTORY', 'db')
embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME', 'all-MiniLM-L6-v2')
chunk_size = 500
chunk_overlap = 50

TOKEN_FILE = 'token.json'
SERVICE_KEY_FILE = 'service_key.json'

def load_documents(ignored_files: List[str] = []) -> List[Document]:
    folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    if folder_id is None:
        print("GOOGLE_DRIVE_FOLDER_ID is not set")
        exit(1)

    loader = GoogleDriveLoader(
        service_account_key=SERVICE_KEY_FILE,
        token_path=TOKEN_FILE,
        folder_id=folder_id,
        recursive=False,
        file_types=["sheet", "document", "pdf"],
    )
    return loader.load()


def process_documents(ignored_files: List[str] = []) -> List[Document]:
    """
    Load documents and split in chunks
    """
    print(f"Loading documents")
    documents = load_documents(ignored_files)
    if not documents:
        print("No new documents to load")
        exit(0)
    print(f"Loaded {len(documents)} new documents")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)")
    return texts

def does_vectorstore_exist(persist_directory: str) -> bool:
    """
    Checks if vectorstore exists
    """
    if os.path.exists(os.path.join(persist_directory, 'index')):
        if os.path.exists(os.path.join(persist_directory, 'chroma-collections.parquet')) and os.path.exists(os.path.join(persist_directory, 'chroma-embeddings.parquet')):
            list_index_files = glob.glob(os.path.join(persist_directory, 'index/*.bin'))
            list_index_files += glob.glob(os.path.join(persist_directory, 'index/*.pkl'))
            # At least 3 documents are needed in a working vectorstore
            if len(list_index_files) > 3:
                return True
    return False

def main():
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    if does_vectorstore_exist(persist_directory):
        # Update and store locally vectorstore
        print(f"Appending to existing vectorstore at {persist_directory}")
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
        collection = db.get()
        texts = process_documents([metadata['source'] for metadata in collection['metadatas']])
        print(f"Creating embeddings. May take some minutes...")
        db.add_documents(texts)
    else:
        # Create and store locally vectorstore
        print("Creating new vectorstore")
        texts = process_documents()
        print(f"Creating embeddings. May take some minutes...")
        db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
    db.persist()
    db = None

    print(f"Ingestion complete! You can now run privateGPT.py to query your documents")


if __name__ == "__main__":
    main()
