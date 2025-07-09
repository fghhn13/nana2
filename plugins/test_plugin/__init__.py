# plugins/test_plugin/__init__.py

from ..base_plugin import BasePlugin
from core.log.logger_config import logger


class TestPlugin(BasePlugin):
    """
    一个用于端到端测试的最简单的插件。
    """

    def get_name(self) -> str:
        # 这个名字必须和AI模拟指令里的'plugin'字段一致
        return "test_plugin"

    def get_commands(self) -> list[str]:
        # 它只有一个命令，叫 'echo'
        return ["echo"]

    def execute(self, command: str, args: dict, controller):
        """
        执行插件的核心逻辑。
        """
        logger.info(f"\n✅ [插件链路] 'test_plugin' 已被成功调用！执行命令: {command}, 参数: {args}\n")

        # 通过控制器，向GUI的消息队列发送一条“任务完成”的消息
        feedback_msg = ("测试插件", f"我被成功执行啦！收到的命令是'{command}'。", "nana_sender")
        controller.view.ui_queue.put(("APPEND_MESSAGE", feedback_msg))


# 主程序会调用这个函数来获取插件实例
def get_plugin():
    return TestPlugin()