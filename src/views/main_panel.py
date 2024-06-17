from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from controllers.qr_generator import qr_generator_controller
from controllers.word_search import word_search_controller

QR_GENERATOR_TAB_TEXT = "QR Generator"
WORD_SEARCH_TAB_TEXT = "Word search"


class ToolBoxMainPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.word_search_tab = TabbedPanelItem(text=WORD_SEARCH_TAB_TEXT)
        self.word_search_tab.add_widget(word_search_controller.view)
        self.add_widget(self.word_search_tab)

        self.qr_generator_tab = TabbedPanelItem(text=QR_GENERATOR_TAB_TEXT)
        self.qr_generator_tab.add_widget(qr_generator_controller.view)
        self.add_widget(self.qr_generator_tab)

        self.set_def_tab(self.word_search_tab)


tool_box_main_panel = ToolBoxMainPanel()
