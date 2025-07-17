from plugins.base_plugin import BasePlugin
from core.log.logger_config import logger
from global_config.settings import AI_NAME, AI_NAME_FRIENDLY
from .notetaker_handle import (
    ensure_notes_folder_exists,
    create_note,
    delete_note,
    list_notes,
    search_notes,
    rename_note,
    get_note_content,
    append_to_note,
)
from .notetaker_ui import open_note_editor, open_notes_window, confirm_delete
from .note_config import (
    CREATE_SUCCESS,
    NOTE_EXISTS,
    DELETE_SUCCESS,
    NOTE_NOT_FOUND,
    NO_NOTES_FOUND,
    SEARCH_RESULTS,
    SEARCH_NONE,
    CANCEL_DELETE,
    PARAM_MISSING,
    APPEND_SUCCESS,
    APPEND_ERROR,
    READING_NOTE,
    NOTE_QA_NOT_FOUND,
    UNKNOWN_QA,
)
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
            "edit_note",
            "delete_note",
            "list_notes",
            "search_notes",
            "rename_note",
            "append_to_note"
        ]

    def on_load(self):
        ensure_notes_folder_exists()

    def execute(self, command: str, args: dict, controller) -> None:
        title = args.get("title") if args else None
        if command == "create_note":
            if not title:
                return
            created = create_note(title)
            msg = (
                CREATE_SUCCESS.format(title=title)
                if created
                else NOTE_EXISTS.format(title=title)
            )
            controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, msg, "nana_sender")))
            if created:
                content = ""
            else:
                content = get_note_content(title) or ""
            run_on_ui(controller, open_note_editor, title, content, controller.view.master)
        elif command == "edit_note":
            if not title:
                return
            content = get_note_content(title)
            if content is None:
                create_note(title)
                content = ""
            run_on_ui(controller, open_note_editor, title, content, controller.view.master)
        elif command == "delete_note":
            if not title:
                return
            confirmed = run_on_ui(controller, confirm_delete, title, controller.view.master)
            if not confirmed:
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, CANCEL_DELETE, "nana_sender")))
                return
            try:
                delete_note(title)
                msg = DELETE_SUCCESS.format(title=title)
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, msg, "nana_sender")))
            except FileNotFoundError:
                err = NOTE_NOT_FOUND.format(title=title)
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME_FRIENDLY, err, "error_sender")))
        elif command == "list_notes":
            notes = list_notes()
            if notes:
                run_on_ui(controller, open_notes_window, notes, controller.view.master)

            else:
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, NO_NOTES_FOUND, "nana_sender")))
        elif command == "search_notes":
            keyword = args.get("keyword") if args else None
            if not keyword:
                return
            notes = search_notes(keyword)
            if notes:
                note_list = "\n".join(f"- {n}" for n in notes)
                msg = SEARCH_RESULTS.format(keyword=keyword, note_list=note_list)
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, msg, "nana_sender")))
                run_on_ui(controller, open_notes_window, notes, controller.view.master)
            else:
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, SEARCH_NONE.format(keyword=keyword), "nana_sender")))
        elif command == "rename_note":
            new_title = args.get("new_title") if args else None
            if not title or not new_title:
                return
            result = rename_note(title, new_title)
            if result.get("status") == "success":
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, result.get("message", ""), "nana_sender")))
            else:
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME_FRIENDLY, result.get("message", ""), "error_sender")))
        elif command == "answer_from_note":
            self.answer_from_note(args or {}, controller)
        elif command == "append_to_note":
            title = args.get("title")
            content_to_add = args.get("content_to_add")

            if not title or not content_to_add:
                # AI一般不会犯这种错，但以防万一
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME_FRIENDLY, PARAM_MISSING, "error_sender")))
                return

            success = append_to_note(title, content_to_add)

            if success:
                # 成功后的反馈
                msg = APPEND_SUCCESS.format(title=title)
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, msg, "nana_sender")))
                # 打开笔记让用户检查
                note_content = get_note_content(title) or ""
                run_on_ui(controller, open_note_editor, title, note_content, controller.view.master)
            else:
                # 失败后的反馈
                controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME_FRIENDLY, APPEND_ERROR.format(title=title), "error_sender")))
        else:
            logger.warning(f"未识别的命令: {command}")

    def answer_from_note(self, args: dict, controller):
        """根据笔记内容回答问题"""
        note_title = args.get("title")
        user_question = args.get("question")

        if not note_title or not user_question:
            controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, UNKNOWN_QA, "nana_sender")))
            return

        controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, READING_NOTE.format(note_title=note_title), "nana_sender")))
        note_content = get_note_content(note_title)

        if note_content:
            qa_prompt = f"""
            你是一个智能助手，请严格根据下面提供的“笔记内容”，回答用户的“问题”。
            要求：
            1. 你的回答必须完全基于提供的“笔记内容”。
            2. 如果笔记内容无法回答问题，请明确说明“根据笔记内容，我无法回答这个问题”。
            3. 不要编造任何笔记中不存在的信息。

            --- 笔记内容 ---
            标题：{note_title}
            {note_content}
            --- 笔记内容结束 ---

            现在，请回答这个问题："{user_question}"
            """

            controller.view.ui_queue.put(
                ("APPEND_MESSAGE", (AI_NAME, "正在思考答案...", "nana_sender"))
            )
            final_answer = controller.detector.ai_service.get_completion(qa_prompt)
            controller.view.ui_queue.put(
                ("APPEND_MESSAGE", (AI_NAME, final_answer, "nana_sender"))
            )
        else:
            controller.view.ui_queue.put(("APPEND_MESSAGE", (AI_NAME, NOTE_QA_NOT_FOUND.format(note_title=note_title), "nana_sender")))


def get_plugin():
    return NoteTakerPlugin()
