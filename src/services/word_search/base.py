from abc import ABC, abstractmethod
from enum import Enum, auto

from models.word_search import WordSearchDetails


class WordSearchService(ABC):
    @abstractmethod
    def search(self, word: str) -> WordSearchDetails:
        ...


class WordSearchStatus(Enum):
    ACCEPTABLE = auto()
    UNACCEPTABLE = auto()
    DOES_NOT_EXIST = auto()
