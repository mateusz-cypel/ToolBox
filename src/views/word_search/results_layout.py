from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from models.word_search import WordSearchDetails
from views.word_search.result_item_card import WordSearchResultItemCard


class WordSearchResultsLayout(ScrollView):
    base_layout_kwargs = {
        "cols": 1,
        "size_hint_y": None,
        "spacing": (0, 20),
        "padding": (10,)
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._layout = GridLayout(**self.base_layout_kwargs)
        self._layout.bind(minimum_height=self._layout.setter('height'))
        self.add_widget(self._layout)

    def update_results(self, search_details: WordSearchDetails):
        self._layout.clear_widgets()
        for details in search_details.word_details:
            layout = WordSearchResultItemCard(details=details, size_hint=(1, None))
            self._layout.add_widget(layout)
