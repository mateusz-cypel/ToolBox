from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from controllers.qr_generator import qr_generator_controller

WINDOW_TITLE = "ToolBox"
WINDOW_WIDTH, WINDOW_HEIGHT = (800, 800)

default_settings = (
    # (section, key-values)
    (
        "window",
        {
            "width": WINDOW_WIDTH,
            "height": WINDOW_HEIGHT,
            "title": WINDOW_TITLE
        }
    ),
)


class ToolBoxApp(App):
    use_kivy_settings = False

    def build_config(self, config):
        for section, key_values in default_settings:
            config.setdefaults(section, key_values)

    def build(self):
        th = TabbedPanelItem(text="QR Generator")
        th.add_widget(qr_generator_controller.view)
        tp = TabbedPanel()
        tp.do_default_tab = False
        tp.add_widget(th)
        return tp

    def on_start(self):
        width = self.config.getint("window", "width")
        height = self.config.getint("window", "height")
        title = self.config.get("window", "title")

        self.root_window.size = (width, height)
        self.root_window.set_title(title)

    def open_settings(self, *largs):
        pass


if __name__ == '__main__':
    ToolBoxApp().run()
