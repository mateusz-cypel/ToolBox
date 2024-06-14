from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from controllers.qr_generator import qr_generator_controller


class ToolBoxMainPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.qr_generator_tab = TabbedPanelItem(text="QR Generator")
        self.qr_generator_tab.add_widget(qr_generator_controller.view)
        self.add_widget(self.qr_generator_tab)

        from kivy.uix.button import Button
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput

        layout = GridLayout(rows=3)

        btn = Button(text="TEST")
        btn.bind(on_press=self.callback)

        self.text_input = TextInput(multiline=False)
        self.label = Label(text="")

        layout.add_widget(self.text_input)
        layout.add_widget(btn)
        layout.add_widget(self.label)

        self.word_checker_tab = TabbedPanelItem(text="Word checker")
        self.word_checker_tab.add_widget(layout)
        self.add_widget(self.word_checker_tab)

        self.set_def_tab(self.qr_generator_tab)

    def callback(self, instance):
        from services.word_search import sjp_word_search
        print(sjp_word_search.search(self.text_input.text))



