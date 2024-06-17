from typing import Callable, Iterable

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from exceptions.word_search import WordSearchEmptyWordError
from validators import EmptyWordValidator

SEARCH_WORD_BUTTON_TEXT = "Search"
WORD_TEXT_INPUT_HINT = "Type your word..."


class WordSearchBarLayout(BoxLayout):
    word_text_input_kwargs = {
        "multiline": False,
        "hint_text": WORD_TEXT_INPUT_HINT,
        "size_hint": (1, None),
    }

    search_word_button_kwargs = {
        "text": SEARCH_WORD_BUTTON_TEXT,
        "size_hint": (None, None),
        "disabled": True,
    }

    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self._word_text_input = TextInput(**self.word_text_input_kwargs)
        self._search_word_button = Button(**self.search_word_button_kwargs)
        self.add_widget(self._word_text_input)
        self.add_widget(self._search_word_button)

        self.bind_on_text_input(
            callbacks=[
                EmptyWordValidator()
            ]
        )

    @property
    def word(self) -> str:
        return str(self._word_text_input.text)

    def bind_on_search_word_button_press(self, callback: Callable) -> None:
        self._search_word_button.bind(on_press=callback)

    def bind_on_text_input(self, callbacks: Iterable[Callable]) -> None:
        def run_callbacks(instance: TextInput, text: str) -> None:
            self._search_word_button.set_disabled(False)
            try:
                for callback in callbacks:
                    callback(text)
            except WordSearchEmptyWordError:
                self._search_word_button.set_disabled(True)
        self._word_text_input.bind(text=run_callbacks)
