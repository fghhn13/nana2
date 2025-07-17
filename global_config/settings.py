# /nana_2/global_config/settings.py
import os

# ==================== 核心：项目的绝对根路径 ====================
# os.path.abspath(__file__) 获取 settings.py 自己的绝对路径
# os.path.dirname(...)       获取它所在的文件夹 (global_config)
# os.path.dirname(...)       再获取上一层文件夹 (nana_2)，这就是我们的项目根目录！
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ==================== 基于根路径，定义所有其他路径 ====================

# --- GUI 相关路径 ---
GUI_DIR = os.path.join(ROOT_DIR, 'Gui')
GUI_CONFIG_DIR = os.path.join(GUI_DIR, 'config')
GUI_WINDOWS_DIR = os.path.join(GUI_DIR, 'windows')
GUI_HANDLE_DIR = os.path.join(GUI_DIR, 'handle')
GUI_LOG_DIR = os.path.join(GUI_DIR, 'log')

# --- 资源文件路径 ---
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets') # 建议把 images 文件夹改名为 assets，更通用
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')

# --- 插件路径 ---
PLUGINS_DIR = os.path.join(ROOT_DIR, 'plugins')

# --- 日志路径 ---
LOG_DIR = os.path.join(ROOT_DIR, 'core', 'log')
# --- 日志格式 ---


# --- AI 相关路径 ---
INTENT_DETECTOR_DIR = os.path.join(ROOT_DIR, 'IntentDetector')
PROMPTS_FILE = os.path.join(INTENT_DETECTOR_DIR, 'ai_service','prompts.json')
#api_url
Api_url="https://dashscope.aliyuncs.com/compatible-mode/v1"


# ==================== 具体的资源文件路径 ====================
IMG_SEND_NORMAL = os.path.join(IMAGES_DIR, "button_normal.png")
IMG_SEND_HOVER = os.path.join(IMAGES_DIR, "button_hover.png")
IMG_SEND_PRESS = os.path.join(IMAGES_DIR, "button_press.png")

# 其他全局配置
APP_VERSION = "2.0.0"
AUTHOR = "你的名字"

# 聊天窗口中显示的名称
USER_NAME = "Fghn"
AI_NAME = "Nana_system"
AI_NAME_FRIENDLY = "Nana"
