from services.word_search.exceptions import WordSearchEmptyWordError


class EmptyWordValidator:
    def __call__(self, text: str):
        if not text:
            raise WordSearchEmptyWordError
