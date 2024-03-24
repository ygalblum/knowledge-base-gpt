""" Abstract all content loaders """
from typing import List

from injector import inject, singleton
from langchain.docstore.document import Document

from knowledge_base_gpt.libs.injector.di import global_injector
from knowledge_base_gpt.libs.settings.settings import Settings
from knowledge_base_gpt.libs.loaders.google_drive_loader import GDriveLoader


@singleton
class Loader():  # pylint:disable=R0903
    """ Abstract all content loaders """

    @inject
    def __init__(self, settings: Settings) -> None:
        mode = settings.content_loader.mode
        match mode:
            case 'google_drive':
                self._content_loader = global_injector.get(GDriveLoader)
            case 'mock':
                pass
            case _:
                pass

    def load_documents(self, ignored_files: List[str]) -> List[Document]:
        """ Load all the documents based on the settings and the ignore list """
        return self._content_loader.load_documents(ignored_files=ignored_files)
