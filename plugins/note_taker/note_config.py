import os
from global_config import settings

# 笔记存储文件夹名
NOTES_FOLDER = "MyNotes"

# 完整笔记目录
NOTES_DIR = os.path.join(settings.PLUGINS_DIR, 'note_taker', NOTES_FOLDER)

# 笔记编辑器默认尺寸
EDITOR_WIDTH = 40
EDITOR_HEIGHT = 60
