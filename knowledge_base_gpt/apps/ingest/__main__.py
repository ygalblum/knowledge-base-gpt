""" Content ingestion application """
from knowledge_base_gpt.libs.injector.di import global_injector
from knowledge_base_gpt.apps.ingest.ingest import Ingestor

global_injector.get(Ingestor).run()
