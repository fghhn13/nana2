# 文件路径: nana_2/plugins/post_it_note/__init__.py

import os
import sys
import json
import subprocess
from plugins.base_plugin import BasePlugin
from core.log.logger_config import logger

# 配置文件现在是插件的一部分
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "nana_note_config.json")
LOCK_FILE = os.path.join(os.path.dirname(__file__), "note.lock")


def load_config():
    """加载配置，如果文件不存在或损坏则返回空字典。"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning(f"[便签插件] 配置文件 '{CONFIG_FILE}' 损坏或无法读取，将创建新的。")
            return {}
    return {}


def save_config(config_data):
    """安全地保存配置。"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        logger.error(f"[便签插件] 保存配置文件失败: {e}")


class PostItNotePlugin(BasePlugin):
    def get_name(self) -> str:
        return "post_it_note"

    def get_commands(self) -> list[str]:
        return ["add_note"]

    def execute(self, command: str, args: dict, controller) -> None:
        if command == "add_note":
            content_to_add = args.get("content")
            if not content_to_add:
                logger.warning("[便签插件] 收到add_note命令，但没有提供内容。")
                return

            config = load_config()
            existing_content = config.get('note_content', '').strip()

            # 判断是追加还是新建，并生成对应回复
            if os.path.exists(LOCK_FILE) and existing_content:
                # 如果窗口已打开且有内容，则追加
                new_content = f"{existing_content}\n- {content_to_add}"
                response_text = "好的！我帮你加上去了。"
            else:
                # 否则，视为新建或在空内容上添加
                new_content = f"- {content_to_add}"
                response_text = "好的，帮你记好啦！"

            config['note_content'] = new_content

            # 设置一个“刷新”信号，并要求自动设为透明模式
            config['force_refresh'] = True
            config['force_transparent'] = True

            save_config(config)

            # 启动便签应用。如果已在运行，它会忽略；如果未运行，它会启动。
            # 无论哪种情况，运行中的应用都会通过定时检查捕捉到`force_refresh`信号。
            app_path = os.path.join(os.path.dirname(__file__), "post_it_note_app.py")

            # 使用 Popen 以非阻塞方式启动，并确保使用正确的 Python 解释器
            # DETACHED_PROCESS 标志让子进程在父进程关闭后也能继续运行
            subprocess.Popen([sys.executable, app_path], creationflags=subprocess.DETACHED_PROCESS, close_fds=True)

            # 在主窗口回应用户
            controller.view.ui_queue.put(("APPEND_MESSAGE", (self.get_name(), response_text, "nana_sender")))


def get_plugin():
    return PostItNotePlugin()