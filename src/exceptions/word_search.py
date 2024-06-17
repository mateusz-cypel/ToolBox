# NETWORK
class WordSearchNetworkError(Exception):
    pass


class WordSearchWordNotFoundError(WordSearchNetworkError):
    def __init__(self, word: str):
        super().__init__(f"The word '{word}' has not been found")


class WordSearchPageNotFoundError(WordSearchNetworkError):
    def __init__(self, url: str):
        super().__init__(f"The page for word searching: {url}' has not been found")


class WordSearchUnknownError(WordSearchNetworkError):
    def __init__(self):
        super().__init__("Unexpected error during word searching")


# DATA FLOW
class WordSearchMissingTagsError(Exception):
    def __init__(self):
        super().__init__("At least one of the arrays has different length")


class WordSearchEmptyWordError(Exception):
    def __init__(self):
        super().__init__("Word was empty")


# MAPPING
class WordSearchStatusMapperUnknownStatusError(Exception):
    def __init__(self, tag_text: str):
        super().__init__(f"Unknown tag text: '{tag_text}' in word search status mapping")
