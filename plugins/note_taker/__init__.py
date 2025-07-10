from plugins.base_plugin import BasePlugin
from core.log.logger_config import logger
from .notetaker_handle import (
    ensure_notes_folder_exists,
    create_note,
    read_note,
    delete_note,
    list_notes,
    search_notes,
)
from .notetaker_ui import open_note_editor, open_notes_window, confirm_delete
import queue


def run_on_ui(controller, func, *args):
    """在主线程执行指定的UI函数并返回结果"""
    q = queue.Queue(maxsize=1)

    def wrapper():
        q.put(func(*args))

    controller.view.ui_queue.put(("RUN_FUNC", wrapper))
    return q.get()


class NoteTakerPlugin(BasePlugin):
    def get_name(self) -> str:
        return "note_taker"

    def get_commands(self) -> list[str]:
        return [
            "create_note",
            "read_note",
            "edit_note",
            "delete_note",
            "list_notes",
            "search_notes",
        ]

    def on_load(self):
        ensure_notes_folder_exists()

    def execute(self, command: str, args: dict, controller) -> None:
        title = args.get("title") if args else None
        if command == "create_note":
            if not title:
                return
            created = create_note(title)
            msg = f"新建笔记 '{title}' 成功。" if created else f"笔记 '{title}' 已存在。"
            controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana", msg, "nana_sender")))
            if created:
                content = ""
            else:
                result = read_note(title)
                if result.get("status") == "success":
                    content = result.get("content", "")
                else:
                    controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana酱", result.get("message", ""), "error_sender")))
                    content = ""
            run_on_ui(controller, open_note_editor, title, content, controller.view.master)
        elif command == "read_note":
            if not title:
                return
            result = read_note(title)
            if result.get("status") == "success":
                content = result.get("content", "")
                if content:
                    msg = f"笔记 '{title}' 的内容如下:\n{content}"
                else:
                    msg = f"笔记 '{title}' 目前是空的。"
                controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana", msg, "nana_sender")))
            else:
                err = result.get("message", "")
                controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana酱", err, "error_sender")))
        elif command == "edit_note":
            if not title:
                return
            result = read_note(title)
            if result.get("status") == "success":
                content = result.get("content", "")
            else:
                create_note(title)
                content = ""
            run_on_ui(controller, open_note_editor, title, content, controller.view.master)
        elif command == "delete_note":
            if not title:
                return
            confirmed = run_on_ui(controller, confirm_delete, title, controller.view.master)
            if not confirmed:
                controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana", "已取消删除。", "nana_sender")))
                return
            try:
                delete_note(title)
                msg = f"已删除笔记 '{title}'。"
                controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana", msg, "nana_sender")))
            except FileNotFoundError:
                err = f"笔记 '{title}' 不存在。"
                controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana酱", err, "error_sender")))
        elif command == "list_notes":
            notes = list_notes()
            if notes:
                run_on_ui(controller, open_notes_window, notes, controller.view.master)

            else:

                controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana", "没有找到任何笔记。", "nana_sender")))
        elif command == "search_notes":
            keyword = args.get("title") if args else None
            if not keyword:
                return
            notes = search_notes(keyword)
            if notes:
                note_list = "\n".join(f"- {n}" for n in notes)
                msg = f"我找到有关于{keyword}的笔记有:\n{note_list}\n你是说哪一个？"
                controller.view.ui_queue.put(("APPEND_MESSAGE", ("Nana", msg, "nana_sender")))
                run_on_ui(controller, open_notes_window, notes, controller.view.master)
            else:
                controller.view.ui_queue.put(
                    (
                        "APPEND_MESSAGE",
                        (
                            "Nana",
                            f"没有找到与 '{keyword}' 相关的笔记。",
                            "nana_sender",
                        ),
                    )
                )
        else:
            logger.warning(f"未识别的命令: {command}")


def get_plugin():
    return NoteTakerPlugin()
