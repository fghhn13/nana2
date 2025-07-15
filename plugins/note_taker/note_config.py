import os
from global_config import settings

# 笔记存储文件夹名
NOTES_FOLDER = "MyNotes"

# 完整笔记目录
NOTES_DIR = os.path.join(settings.PLUGINS_DIR, 'note_taker', NOTES_FOLDER)

# 笔记编辑器默认尺寸
EDITOR_WIDTH = 40
EDITOR_HEIGHT = 60

# --- 消息模板 ---
# 重命名笔记相关
RENAME_NOTE_NOT_FOUND = "错误：找不到名为 '{old_title}' 的笔记。"
RENAME_NOTE_EXISTS = "错误：名为 '{new_title}' 的笔记已经存在了，换个新名字吧！"
RENAME_NOTE_SUCCESS = "成功将笔记 '{old_title}' 重命名为 '{new_title}'！"
RENAME_NOTE_ERROR = "修改笔记名称时发生意外：{e}"

# 在笔记中追加内容时的时间戳前缀
NOTE_APPEND_PREFIX = "--- (Nana帮你记在 {timestamp}) ---"

# 插件交互消息
CREATE_SUCCESS = "新建笔记 '{title}' 成功。"
NOTE_EXISTS = "笔记 '{title}' 已存在。"
DELETE_SUCCESS = "已删除笔记 '{title}'。"
NOTE_NOT_FOUND = "笔记 '{title}' 不存在。"
NO_NOTES_FOUND = "没有找到任何笔记。"
SEARCH_RESULTS = "我找到了和 '{keyword}' 相关的笔记有这些哦：\n{note_list}\n需要我帮你打开哪一个吗？"
SEARCH_NONE = "没有找到与 '{keyword}' 相关的笔记。"
CANCEL_DELETE = "已取消删除。"
PARAM_MISSING = "哎呀，我好像忘记要记什么或者记在哪里了..."
APPEND_SUCCESS = "我已经帮你把内容添加到《{title}》里啦！"
APPEND_ERROR = "糟糕...在给《{title}》做笔记的时候出错了。"
READING_NOTE = "正在翻阅《{note_title}》笔记..."
NOTE_QA_NOT_FOUND = "抱歉主人，我找不到名为《{note_title}》的笔记哦。"
UNKNOWN_QA = "抱歉，我没有理解要查哪个笔记或具体问题是什么。"
