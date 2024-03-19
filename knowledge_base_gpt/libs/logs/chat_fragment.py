from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import uuid

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.documents.base import Document


class ChatFragment(ABC):

    def __init__(self, answer: Dict[str, Any], callback_handler: BaseCallbackHandler, chat_identifier: Optional[str] = None) -> None:
        super().__init__()
        if chat_identifier is None:
            chat_identifier = str(uuid.uuid4())
        self.chat_identifier = chat_identifier
        self.question = answer['question']
        self.generated_question = answer['generated_question']
        self.answer = answer['answer']
        self.source_documents = self._calculate_source_documents(answer['source_documents'])
        self.metrics = self._calculate_metrics(callback_handler)

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

    @abstractmethod
    def _calculate_metrics(self, callback_handler: BaseCallbackHandler):
        pass

    def to_json(self) -> dict:
        return {
            "chat_identifier": self.chat_identifier,
            "question": self.question,
            "generated_question": self.generated_question,
            "answer": self.answer,
            "source_documents": self.source_documents,
            "metrics": self.metrics
        }
