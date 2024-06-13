class TextMaxLengthError(Exception):
    def __init__(self, text_length: int, max_length: int):
        super().__init__(
            f"The text reached out the limit of characters which is {max_length}. "
            f"Current text length is {text_length}")
