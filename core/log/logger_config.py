# 我看到的内容
import logging
from logging.handlers import RotatingFileHandler
from global_config.settings import LOG_DIR
import os

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 定义日志文件的路径
LOG_FILE_PATH = os.path.join(LOG_DIR, 'nana.log')


# 创建一个logger
logger = logging.getLogger('nana_logger')
logger.setLevel(logging.INFO)

# 创建文件处理器
file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=1024 * 1024 * 5, backupCount=5, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 创建控制台处理器
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(module)s.%(funcName)s:%(lineno)d - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# 添加处理器到logger
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)