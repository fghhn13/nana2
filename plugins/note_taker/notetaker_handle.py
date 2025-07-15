import os
from datetime import datetime
from .note_config import (
    NOTES_DIR,
    NOTES_FOLDER,
    RENAME_NOTE_NOT_FOUND,
    RENAME_NOTE_EXISTS,
    RENAME_NOTE_SUCCESS,
    RENAME_NOTE_ERROR,
    NOTE_APPEND_PREFIX,
)

def ensure_notes_folder_exists():
    """确保笔记文件夹存在。如不存在则尝试创建；
    若创建失败，则在插件目录下新建一个 MyNotes 文件夹。"""
    global NOTES_DIR
    if os.path.exists(NOTES_DIR):
        return
    try:
        os.makedirs(NOTES_DIR)
    except Exception:
        fallback_dir = os.path.join(os.path.dirname(__file__), NOTES_FOLDER)
        os.makedirs(fallback_dir, exist_ok=True)
        NOTES_DIR = fallback_dir

def get_note_path(note_name: str) -> str:
    return os.path.join(NOTES_DIR, f"{note_name}.txt")

def list_notes() -> list[str]:
    if not os.path.exists(NOTES_DIR):
        return []
    return sorted(
        os.path.splitext(f)[0]
        for f in os.listdir(NOTES_DIR)
        if f.endswith(".txt")
    )

def create_note(note_name: str) -> bool:
    ensure_notes_folder_exists()
    note_path = get_note_path(note_name)
    if os.path.exists(note_path):
        return False
    with open(note_path, "w", encoding="utf-8"):
        pass
    return True

def delete_note(note_name: str) -> None:
    os.remove(get_note_path(note_name))



def search_notes(keyword: str) -> list[str]:
    """根据关键字在标题或内容中搜索笔记"""
    ensure_notes_folder_exists()
    results: list[str] = []
    keyword_lower = keyword.lower()
    for f in os.listdir(NOTES_DIR):
        if not f.endswith(".txt"):
            continue
        note_name = os.path.splitext(f)[0]
        path = os.path.join(NOTES_DIR, f)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except Exception:
            content = ""
        if keyword_lower in note_name.lower() or keyword_lower in content.lower():
            results.append(note_name)
    return sorted(results)


def rename_note(old_title: str, new_title: str) -> dict:
    """重命名现有笔记"""
    ensure_notes_folder_exists()
    old_file_path = get_note_path(old_title)
    new_file_path = get_note_path(new_title)

    if not os.path.exists(old_file_path):
        return {"status": "error", "message": RENAME_NOTE_NOT_FOUND.format(old_title=old_title)}

    if os.path.exists(new_file_path):
        return {"status": "error", "message": RENAME_NOTE_EXISTS.format(new_title=new_title)}

    try:
        os.rename(old_file_path, new_file_path)
        print(f"成功将笔记 '{old_title}' 重命名为 '{new_title}'")
        return {"status": "success", "message": RENAME_NOTE_SUCCESS.format(old_title=old_title, new_title=new_title)}
    except Exception as e:
        print(f"重命名文件时发生错误: {e}")
        return {"status": "error", "message": RENAME_NOTE_ERROR.format(e=e)}


def get_note_content(title: str) -> str | None:
    """根据标题获取笔记的原始内容。如果文件不存在则返回 None。"""
    safe_title = title.replace("..", "").replace("/", "").replace("\\", "")
    filepath = os.path.join(NOTES_DIR, f"{safe_title}.txt")

    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading note '{title}': {e}")
            return None
    else:
        return None


def append_to_note(title: str, content: str) -> bool:
    """
    在指定笔记的末尾追加内容。如果笔记不存在，则创建它。
    返回操作是否成功。
    """
    ensure_notes_folder_exists()
    note_path = get_note_path(title)

    # 格式化要追加的内容
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    formatted_content = f"\n\n{NOTE_APPEND_PREFIX.format(timestamp=timestamp)}\n{content}\n"

    try:
        # 使用 'a' 模式来追加内容，文件不存在会自动创建
        with open(note_path, "a", encoding="utf-8") as f:
            f.write(formatted_content)
        return True
    except Exception as e:
        # 你可以在这里用 logger 记录详细错误
        print(f"追加笔记时发生错误: {e}")
        return False