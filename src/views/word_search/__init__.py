from typing import Callable

from kivy.uix.boxlayout import BoxLayout

from models.word_search import WordSearchDetails
from views.word_search.result_item_card import WordSearchResultItemCard
from views.word_search.results_layout import WordSearchResultsLayout
from views.word_search.search_layout import WordSearchBarLayout


class WordSearchView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self._results_layout = WordSearchResultsLayout()
        self._search_layout = WordSearchBarLayout(size_hint=(1, None))
        self.add_widget(self._results_layout)
        self.add_widget(self._search_layout)

    @property
    def word(self) -> str:
        return self._search_layout.word

    def update_view(self, search_details: WordSearchDetails) -> None:
        self._results_layout.update_results(search_details)

    def bind_on_search_word_button_press(self, callback: Callable) -> None:
        self._search_layout.bind_on_search_word_button_press(callback)


word_search_view = WordSearchView()

