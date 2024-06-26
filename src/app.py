from kivy.app import App

from views.main_panel import tool_box_main_panel, ToolBoxMainPanel

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

    def build_config(self, config) -> None:
        for section, key_values in default_settings:
            config.setdefaults(section, key_values)

    def build(self) -> ToolBoxMainPanel:
        return tool_box_main_panel

    def on_start(self) -> None:
        width = self.config.getint("window", "width")
        height = self.config.getint("window", "height")
        title = self.config.get("window", "title")

        self.root_window.size = (width, height)
        self.root_window.set_title(title)

    def open_settings(self, *largs) -> None:
        pass


if __name__ == '__main__':
    ToolBoxApp().run()
