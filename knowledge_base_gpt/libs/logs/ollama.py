import json
from typing import List, Dict, Any, Optional
import uuid

from langchain_core.documents.base import Document

from knowledge_base_gpt.libs.gpt.ollama_info import OllamaMetrics, OllamaCallbackHandler


class OllamaChatFragment():
    def __init__(self, answer: Dict[str, Any], callback_handler: OllamaCallbackHandler, chat_identifier: Optional[str] = None) -> None:
        if chat_identifier is None:
            chat_identifier = str(uuid.uuid4())

        self.chat_identifier = chat_identifier
        self.question = answer['question']
        self.generated_question = answer['generated_question']
        self.answer = answer['answer']
        self.source_documents = self._calculate_source_documents(answer['source_documents'])
        self.metrics = self._calculate_metrics(callback_handler.metrics)

    def to_json(self) -> dict:
        return {
            "chat_identifier": self.chat_identifier,
            "question": self.question,
            "generated_question": self.generated_question,
            "answer": self.answer,
            "source_documents": self.source_documents,
            "metrics": self.metrics
        }

    @staticmethod
    def _calculate_source_documents(source_documents: List[Document]) -> List[dict]:
        scanned_documents = {}
        for document in source_documents:
            metadata = document.metadata
            source_fragments = metadata['source'].split('/')
            file_id = source_fragments[-2] if len(source_fragments) > 2 else metadata['source']
            source_document = scanned_documents.get('file_id')
            if source_document:
                existing_pages = set(source_document['pages'])
                existing_pages.add(metadata['page'])
                source_document['pages'] = list(existing_pages)
            else:
                source_document = {
                    "source": metadata['source'],
                    "title": metadata['title'],
                    "pages": [metadata['page']]
                }
            scanned_documents[file_id] = source_document
        return list(scanned_documents.values())

    @staticmethod
    def _calculate_metrics(metrics: List[OllamaMetrics]):
        ret = {}
        answer_index = 0
        if len(metrics) > 1:
            ret['question_generation'] = metrics[0].to_json()
            answer_index = 1
        ret['answer_generation'] = metrics[answer_index].to_json()
        return ret


class OllamaChatLogExporter():
    def __init__(self, path: str):
        self._path = path

    def save_chat_log(self, chat_fragment: OllamaChatFragment):
        with open(self._path, "a+") as f:
            f.write(f"{json.dumps(chat_fragment.to_json())}\n")
