
from plugins.base_plugin import BasePlugin
import os
import json
import subprocess

class ExeStarterPlugin(BasePlugin):
    def get_name(self) -> str:
        return "exe_starter"

    def get_commands(self) -> list[str]:
        return ["start_app"]

    def execute(self, command: str, args: dict, controller) -> None:
        if command == "start_app":
            app_name = args.get("app_name")
            if not app_name:
                print("错误：未指定应用名称。")
                return

            # 读取“地址簿”
            paths_file = os.path.join(os.path.dirname(__file__), "app_paths.json")
            try:
                with open(paths_file, 'r', encoding='utf-8') as f:
                    app_paths = json.load(f)
            except FileNotFoundError:
                print(f"错误：找不到应用地址簿 app_paths.json。")
                return

            # 查找并启动应用
            app_path = app_paths.get(app_name)
            if app_path and os.path.exists(app_path):
                try:
                    subprocess.Popen(app_path)
                    print(f"正在为您启动 {app_name}...")
                except Exception as e:
                    print(f"启动 {app_name} 失败: {e}")
            else:
                print(f"错误：在地址簿中未找到应用 '{app_name}' 或路径无效。")

def get_plugin():
    return ExeStarterPlugin()