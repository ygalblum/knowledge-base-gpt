#!/usr/bin/env python3
import os
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders import GoogleDriveLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from libs.common import constants


# Load environment variables
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
    docs = loader.load()
    return [doc for doc in docs if doc.metadata['source'] not in ignored_files]


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
    return os.path.exists(os.path.join(persist_directory, 'chroma.sqlite3'))

def main():
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name=constants.embeddings_model_name)

    if does_vectorstore_exist(constants.persist_directory):
        # Update and store locally vectorstore
        print(f"Appending to existing vectorstore at {constants.persist_directory}")
        db = Chroma(persist_directory=constants.persist_directory, embedding_function=embeddings, client_settings=constants.CHROMA_SETTINGS)
        collection = db.get()
        texts = process_documents(set(metadata['source'] for metadata in collection['metadatas']))
        print(f"Creating embeddings. May take some minutes...")
        db.add_documents(texts)
    else:
        # Create and store locally vectorstore
        print("Creating new vectorstore")
        texts = process_documents()
        print(f"Creating embeddings. May take some minutes...")
        db = Chroma.from_documents(texts, embeddings, persist_directory=constants.persist_directory)
    db.persist()
    db = None

    print(f"Ingestion complete! You can now run privateGPT.py to query your documents")


if __name__ == "__main__":
    main()
