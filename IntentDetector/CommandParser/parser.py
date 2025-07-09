# IntentDetector/CommandParser/parser_main.py

from .Judge.validator import CommandValidator
from .translate.formatter import CommandFormatter
from core.log.logger_config import logger


class CommandParser:
    """
    命令解析器的主管。
    协调“质检部”和“翻译部”完成整个解析流程。
    """

    def __init__(self):
        self.validator = CommandValidator()
        self.formatter = CommandFormatter()
        logger.info("[解析器主管] 已初始化，下辖'质检部'和'翻译部'。")

    def parse(self, raw_command_from_ai: dict) -> dict:
        # 第一步：交给“质检部”进行审查
        is_valid, message = self.validator.validate(raw_command_from_ai)

        if not is_valid:
            # 如果质检不通过，直接打回，并生成一个安全的回退指令
            logger.info(f"[解析器主管] 质检失败: {message}")
            return self._create_fallback_command(message)

        # 第二步：如果质检通过，交给“翻译部”进行标准化
        logger.info(f"[解析器主管] 质检通过: {message}")
        formatted_command = self.formatter.format(raw_command_from_ai)

        return formatted_command

    def _create_fallback_command(self, error_message: str) -> dict:
        return {
            "plugin": None,
            "command": None,
            "args": None,
            "response": f"呜哇，我的大脑好像短路了... ({error_message}) 我已经把问题记下来了！"
        }