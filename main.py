# /nana_2/main.py

# =================== 新增的“开天辟地”代码 ===================
import sys
import os

# 动态地将项目根目录(nana_2)的父级目录添加到Python的模块搜索路径中
# 这样无论从哪里启动，都能正确找到所有模块
project_root = os.path.dirname(os.path.abspath(__file__))
# F:\...\nana_2
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 现在Python的“通讯录”里已经有了我们项目的地址，下面的导入将万无一失
# =============================================================

from core.log.logger_config import logger
import tkinter as tk
import threading
from Gui.windows.main_window import MainWindow
from IntentDetector.main_detector import MainDetector
from CommandExecutor.cmd_main import CommandExecutor
from core.plugin_system.plugin_manager import PluginManager



# 【注意】: 下面的 AppController 和 if __name__ == "__main__": 部分，
# 和我上次发给你的完全一样，保持不变即可！

class AppController:
    """
    应用程序的总司令。
    负责初始化所有核心模块，并协调它们之间的工作。
    """

    def __init__(self):
        self.view = None
        # 【注意】这里的导入现在会因为上面的 sys.path 修改而正常工作
        from IntentDetector.main_detector import MainDetector
        from CommandExecutor.cmd_main import CommandExecutor
        from core.plugin_system.plugin_manager import PluginManager

        # 1. 创建插件管理器并加载所有插件
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all_plugins()

        # 2. 创建命令执行器，让它使用 PluginManager 中的插件
        self.executor = CommandExecutor(self.plugin_manager)

        # 3. 创建意图检测器，并把执行器“注入”给它
        self.detector = MainDetector(command_executor=self.executor)

        # --- 接线完成！现在它们俩已经成功关联啦！---

        self.conversation_history = []

    def set_view(self, view: MainWindow):
        """让控制器能够访问到GUI实例，以便操作UI队列。"""
        self.view = view

    def start_app(self):
        """应用启动时，由 main 函数调用。"""
        welcome_msg = ("Nana酱", "主人，所有模块已连接，大脑已上线！请下达指令吧！", "nana_sender")
        self.view.ui_queue.put(("APPEND_MESSAGE", welcome_msg))

    def process_user_input(self, user_text: str):
        """这是从GUI的EventHandler接收用户输入的唯一入口。"""
        user_msg = ("你", user_text, "user_sender")
        self.view.ui_queue.put(("APPEND_MESSAGE", user_msg))
        self.conversation_history.append({"role": "user", "content": user_text})
        thread = threading.Thread(target=self._run_backend_process)
        thread.daemon = True
        thread.start()

    def _run_backend_process(self):
        """运行所有后端逻辑（检测、执行），这个方法在子线程中被调用。"""
        self.view.ui_queue.put(("SET_STATE", "disabled"))
        command = self.detector.detect_and_parse(self.conversation_history)
        ai_response = command.get("response")
        if ai_response:
            response_msg = ("Nana酱", ai_response, "nana_sender")
            self.view.ui_queue.put(("APPEND_MESSAGE", response_msg))
            self.conversation_history.append({"role": "assistant", "content": ai_response})
        if command.get("intent") == "needs_clarification":
            # 只显示反问语句，不调用任何插件
            self.view.ui_queue.put(("SET_STATE", "enabled"))
            return

        if command.get("command") == "answer_from_note":
            note_plugin = self.plugin_manager.plugins.get("note_taker")
            if note_plugin and hasattr(note_plugin, "answer_from_note"):
                note_plugin.answer_from_note(command.get("args", {}) or {}, self)
        else:
            self.executor.execute_command(command, self)
        self.view.ui_queue.put(("SET_STATE", "enabled"))

    def on_app_exit(self):
        """当GUI关闭时被调用"""
        logger.info("[总司令] 收到关闭信号，应用即将退出。")


# --- 程序主入口 ---
if __name__ == "__main__":
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    # 为了让上面的 sys.path 修改能对所有模块生效，
    # 我们把原来在顶部的 import 移到这里来
    from Gui.windows.main_window import MainWindow

    root = tk.Tk()
    controller = AppController()
    main_view = MainWindow(root, controller)
    controller.set_view(main_view)

    # 删除了原来的 controller.start_app()，因为AppController的__init__里并没有这个方法
    # 启动逻辑应该由AppController自己管理，或者由一个更上层的逻辑调用
    # 在这里，我们让MainWindow的初始化去触发start_app
    main_view.master.after(100, controller.start_app)
    root.mainloop()
