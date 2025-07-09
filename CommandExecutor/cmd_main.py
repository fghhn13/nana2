# CommandExecutor/cmd_main.py
from core.log.logger_config import logger


class CommandExecutor:
    """
    命令执行中心（Command Executor）。
    只负责根据指令调用已加载的插件执行任务。
    """

    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugins = plugin_manager.plugins

    def refresh_commands(self):
        """从 PluginManager 刷新插件映射。"""
        self.plugins = self.plugin_manager.plugins


    @property
    def loaded_plugins(self) -> dict:
        """
        一个公开的属性，让外部可以获取到所有已加载的插件。
        就像一个透明的展示柜，展示着所有可用的工具。
        """
        return self.plugins

    def execute_command(self, command: dict, controller):
        """
        接收指令并执行。这是提供给外部调用的主方法。
        """
        plugin_name = command.get('plugin')

        if not plugin_name:
            # 如果指令没有指定插件，说明可能是一条纯聊天或无需执行的消息
            logger.info(f"[执行器] 收到无需执行的指令。")
            return

        logger.info(f"[执行器] 收到指令，需要插件 '{plugin_name}' 来执行。")

        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            cmd_name = command.get('command')
            cmd_args = command.get('args', {})
            logger.info(
                f"[执行器] 调用插件 '{plugin_name}' 执行命令 '{cmd_name}'，参数: {cmd_args}"
            )
            try:
                plugin.execute(cmd_name, cmd_args, controller)
            except Exception as e:
                logger.error(
                    f"[执行器] 插件 '{plugin_name}' 执行命令 '{cmd_name}' 失败: {e}",
                    exc_info=True,
                )
        else:
            logger.info(f"[执行器] 错误：找不到名为 '{plugin_name}' 的插件。")

