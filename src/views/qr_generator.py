from typing import Callable, Iterable

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from validators import TextLengthValidator


class QRGeneratorView(GridLayout):
    QR_GENERATE_BUTTON_TEXT = "Generate QR"
    QR_LABEL_OUTPUT_TEXT = "The latest generated QR: {date}"
    QR_LABEL_OUTPUT_TEXT_DEFAULT = "Not generated yet"

    def __init__(self):
        super().__init__(cols=2)
        # left side
        self.message_text_input = TextInput(multiline=True)

        # right side
        self.qr_image = Image(source=None)
        self.qr_label = Label(
            text=QRGeneratorView.QR_LABEL_OUTPUT_TEXT_DEFAULT,
            size_hint_y=None,
        )
        self.qr_generate_button = Button(
            text=QRGeneratorView.QR_GENERATE_BUTTON_TEXT,
            size_hint_y=None,
        )

        self.right_layout = GridLayout(rows=3)
        self.right_layout.add_widget(self.qr_image)
        self.right_layout.add_widget(self.qr_label)
        self.right_layout.add_widget(self.qr_generate_button)

        # add to main widget
        self.add_widget(self.message_text_input)
        self.add_widget(self.right_layout)

    @property
    def message(self) -> str:
        return str(self.message_text_input.text)

    def update_view(self, source: str, updated_at: str) -> None:
        self.update_qr_label(updated_at)
        self.qr_image.source = source
        self.qr_image.reload()
        self.qr_image.texture_update()

    def update_qr_label(self, updated_at: str) -> None:
        self.qr_label.text = QRGeneratorView.QR_LABEL_OUTPUT_TEXT.format(date=updated_at)

    def bind_on_text_input(self, callbacks: Iterable[Callable]) -> None:
        def run_callbacks(instance: TextInput, text: str) -> None:
            for callback in callbacks:
                callback(text)
        self.message_text_input.bind(text=run_callbacks)

    def bind_on_qr_generate_button_press(self, callback: Callable) -> None:
        self.qr_generate_button.bind(on_press=callback)


qr_generator_view = QRGeneratorView()
qr_generator_view.bind_on_text_input(
    callbacks=[TextLengthValidator(max_length=4098)]
)

