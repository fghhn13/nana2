import os
from Gui.config import gui_config

NOTES_FOLDER = "MyNotes"

# Ensure notes directory exists
NOTES_DIR = gui_config.NOTES_DIR

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

def read_note(note_name: str) -> str:
    with open(get_note_path(note_name), "r", encoding="utf-8") as f:
        return f.read()


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

