from typing import Callable

from services.word_search import sjp_word_search_service
from services.word_search.base import WordSearchService
from views.word_search import WordSearchView, word_search_view


class WordSearchController:
    def __init__(self, view: WordSearchView, word_search: WordSearchService):
        self._view = view
        self._view.bind_on_search_word_button_press(self.search_word)
        self._word_search = word_search

    @property
    def view(self) -> WordSearchView:
        return self._view

    @property
    def search_word(self) -> Callable:
        def callback(instance):
            word = self._view.word
            details = self._word_search.search(word)
            self._view.update_view(details)
        return callback


word_search_controller = WordSearchController(
    view=word_search_view,
    word_search=sjp_word_search_service,
)
