from exceptions.qr_generator import TextMaxLengthError


class TextLengthValidator:
    def __init__(self, max_length: int):
        self.max_length = max_length

    def __call__(self, text: str):
        text_length = len(text)
        if text_length > self.max_length:
            raise TextMaxLengthError(text_length=text_length, max_length=self.max_length)
