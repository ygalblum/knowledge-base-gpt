""" Content loader from Google Drive """
from typing import List

from injector import inject, singleton
from langchain.docstore.document import Document
from langchain_community.document_loaders import GoogleDriveLoader

from knowledge_base_gpt.libs.settings.settings import Settings


@singleton
class GDriveLoader():  # pylint:disable=R0903
    """ Content loader from Google Drive """

    @inject
    def __init__(self, settings: Settings) -> None:
        self._service_key_file = settings.google_drive.service_key_file
        self._folder_id = settings.google_drive.folder_id

    def load_documents(self, ignored_files: List[str]) -> List[Document]:
        """ Load the documents based on the settings and the ignore list """
        if not self._folder_id:
            return []

        loader_args = {
            "folder_id": self._folder_id,
            "recursive": False,
            "file_types": ["sheet", "document", "pdf"],
        }
        if self._service_key_file:
            loader_args['service_account_key'] = self._service_key_file

        loader = GoogleDriveLoader(**loader_args)
        docs = loader.load()
        return [doc for doc in docs if doc.metadata['source'] not in ignored_files]
