# config/app_config.py
import os

# --- 路径管理 (Path Management) ---
# 项目的根目录 (The root directory of the project)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 基于根目录构建其他路径 (Build other paths based on the root directory)
IMAGES_DIR = os.path.join(ROOT_DIR, "images")
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
NOTES_DIR = os.path.join(ROOT_DIR, "MyNotes") # 笔记文件夹

# --- 文件名管理 (File Name Management) ---
PERSONA_FILE = os.path.join(ROOT_DIR, "nana_persona.txt")
PROMPTS_FILE = os.path.join(CONFIG_DIR, "prompts.json")
IMG_SEND_NORMAL = os.path.join(IMAGES_DIR, "button_normal.png")
IMG_SEND_HOVER = os.path.join(IMAGES_DIR, "button_hover.png")
IMG_SEND_PRESS = os.path.join(IMAGES_DIR, "button_press.png")

# --- UI 字符串常量 (UI String Constants) ---
# 窗口标题 (Window Titles)
APP_TITLE = "Nana的AI记事本 ✨"
NOTES_WINDOW_TITLE = "我的笔记"
NOTE_EDITOR_TITLE_PREFIX = "编辑笔记："
SAVE_BUTTON_TEXT = "保存笔记"
# 发送者名称 (Sender Names)
SENDER_USER = "你"
SENDER_AI = "Nana"
SENDER_AI_ERROR = "Nana酱"

# UI 文本 (UI Texts)
INPUT_PLACEHOLDER = "在这里输入消息..."
INITIAL_GREETING = "有什么事吗，喵？...我已经准备好为你服务啦！"
CONFIRM_SAVE_TITLE = "保存成功"
CONFIRM_SAVE_MESSAGE = "笔记 '{note_name}' 已保存！"
ERROR_SAVE_TITLE = "保存失败"
ERROR_SAVE_MESSAGE = "保存笔记时发生错误：{e}"
AI_THINKING_MESSAGE = "正在思考中..." # AI思考时的提示信息
CONFIRM_DELETE_TITLE = "确认删除"
CONFIRM_DELETE_MESSAGE = "确定要删除笔记 '{note_name}' 吗？"

#颜色
# --- 主题颜色 ---
BG_MAIN = "#212121"
FG_TEXT = "#cbcbcb"
BG_INPUT = "#3a3a3a"
BG_LISTBOX = "#202020"
FG_LISTBOX = "#e0e0e0"
BG_INPUT_DISABLED = "#303030"  # 新增：输入框禁用时的背景色 (可以选一个更暗的颜色)
FG_TEXT_DISABLED = "#6e6e6e"   # 新增：输入框禁用时的文字颜色 (灰色)
# --- 控件颜色 ---
BG_BUTTON = "#424242"
FG_BUTTON = "white"
BUTTON_ACTIVE_BG = "#555555"

# --- 选择与高亮 ---
SELECT_BG_LISTBOX = "#3a3a3a"
SELECT_FG_LISTBOX = "white"
CURSOR_COLOR = "white"

# --- 字体设置 ---
GENERAL_FONT_FAMILY = "Microsoft YaHei"
GENERAL_FONT_SIZE = 14