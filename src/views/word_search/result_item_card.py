from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from models.word_search import WordDetails


class WordSearchResultItemCard(GridLayout):
    SEARCHED_WORD_LABEL_TEXT = "Searched word:"
    BASE_WORD_LABEL_TEXT = "Base word:"
    STATUS_LABEL_TEXT = "Status:"
    DESCRIPTION_LABEL_TEXT = "Description:"

    result_header_labels_kwargs = {
        "bold": True,
    }
    result_value_labels_kwargs = {}
    result_text_input_kwargs = {
        "disabled": True,
        "multiline": True,
    }

    def __init__(self, details: WordDetails, **kwargs):
        super().__init__(cols=2, **kwargs)
        # first row
        layout = GridLayout(rows=3, size_hint_y=None, spacing=(0,10))
        for header, value in (
            (self.SEARCHED_WORD_LABEL_TEXT, details.searched_for),
            (self.BASE_WORD_LABEL_TEXT, details.base),
            (self.STATUS_LABEL_TEXT, details.status),
        ):
            label = self.LabeledLabel(header=header, value=value, spacing=(0, 5))
            layout.add_widget(label)

        # second row
        description = self.LabeledTextInput(
            header=self.DESCRIPTION_LABEL_TEXT,
            value=details.description,
            spacing=(0, 5),
            size_hint_y=None
        )

        self.add_widget(layout)
        self.add_widget(description)

    class LabeledTextInput(GridLayout):
        text_input_kwargs = {
            "disabled": True,
            "multiline": True,
            "size_hint_y": None,
        }

        def __init__(self, header, value, **kwargs):
            super().__init__(cols=1, **kwargs)
            self.add_widget(Label(text=header, bold=True))
            self.add_widget(TextInput(text=value, **self.text_input_kwargs))

    class LabeledLabel(GridLayout):
        def __init__(self, header, value, **kwargs):
            super().__init__(rows=1, **kwargs)
            self.add_widget(Label(text=header, bold=True))
            self.add_widget(Label(text=value))
