from plugins.base_plugin import BasePlugin
import os
import sys
import subprocess

class ColorPickerPlugin(BasePlugin):
    def get_name(self) -> str:
        return "color_picker"

    def get_commands(self) -> list[str]:
        return ["open_color_picker"]

    def execute(self, command: str, args: dict, controller) -> None:
        if command == "open_color_picker":
            app_path = os.path.join(os.path.dirname(__file__), "color_picker_app.py")
            subprocess.Popen([sys.executable, app_path])


def get_plugin():
    return ColorPickerPlugin()
