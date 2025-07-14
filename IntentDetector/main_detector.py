# IntentDetector/main_detector.py

# 导入我们刚刚创建的 AI 服务模块
from .ai_service.ai_service import AIService
from .CommandParser.parser import CommandParser
from core.log.logger_config import logger

class MainDetector:
    """
    意图识别模块的主控制器 (部门主管).
    负责协调 AI服务 和 (未来的)命令解析器.
    """

    def __init__(self, command_executor):
        """
        初始化时，必须传入一个 CommandExecutor 的实例。
        就像给检测器配备了一个可以直接沟通的执行器。
        """
        self.ai_service = AIService()
        # self.command_parser = CommandParser()
        self.command_executor = command_executor  # 把执行器实例存起来
        logger.info("[检测器] 意图检测器已初始化，并与命令执行器建立连接。")

    def detect_and_parse(self, conversation_history: list):
        logger.info("[检测器] 开始检测用户意图...")

        active_plugins = self.command_executor.loaded_plugins
        raw_command = self.ai_service.recognize_command(
            conversation_history,
            loaded_plugins=active_plugins
        )
        logger.info(f"[检测器] 从AI服务收到原始指令: {raw_command}")


        final_command = raw_command

        logger.info("[检测器] 意图检测流程完成。")
        return final_command