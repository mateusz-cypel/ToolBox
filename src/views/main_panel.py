from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from controllers.qr_generator import qr_generator_controller


class ToolBoxMainPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.qr_generator_tab = TabbedPanelItem(text="QR Generator")
        self.qr_generator_tab.add_widget(qr_generator_controller.view)
        self.add_widget(self.qr_generator_tab)

        self.set_def_tab(self.qr_generator_tab)
