import os
from chromadb.config import Settings

persist_directory = os.environ.get('PERSIST_DIRECTORY', 'db')
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    is_persistent=True,
    persist_directory=persist_directory,
    anonymized_telemetry=False
)
