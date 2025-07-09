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

        # --- 第 2 步：(即将到来) 让“参谋部”(CommandParser)去审查和翻译指令 ---
        # # 这一步我们先注释掉，等建好 CommandParser 再启用
        # clean_command = self.command_parser.parse(raw_command_from_ai)
        # logger.info(f"[检测器] 经过解析器处理后的干净指令: {clean_command}")

        # 在“参谋部”建好之前，我们先直接把原始指令当作最终结果返回
        #
        final_command = raw_command

        logger.info("[检测器] 意图检测流程完成。")
        return final_command