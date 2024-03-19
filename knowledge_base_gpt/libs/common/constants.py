import os
from pathlib import Path

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")

PROJECT_ROOT_PATH: Path = Path(__file__).parents[3]
