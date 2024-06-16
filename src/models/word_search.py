from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class WordDetails:
    searched_for: str
    base: str
    status: str
    description: str


@dataclass(frozen=True)
class WordSearchDetails:
    word_details: Iterable[WordDetails]
