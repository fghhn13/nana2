# /nana_2/plugins/base_plugin.py

import os
import json
from global_config import settings
from core.log.logger_config import logger


class BasePlugin:
    """
    【插件基类 - 所有插件的“父上大人”】

    这是一个抽象基类（Abstract Base Class），定义了所有插件都必须拥有的“标准行为”。
    任何想要被我们的 PluginManager 识别和管理的插件，都必须继承这个类，
    并实现它要求的所有方法。

    这就像是加入一个俱乐部，必须遵守的会员章程一样！
    """

    def get_name(self) -> str:
        """
        【必须实现】返回插件的唯一名称 (小写蛇形命名法, e.g., 'note_taker')。
        这个名字将作为插件的“身份证”，用于加载、卸载和调用。
        """
        raise NotImplementedError("每个插件都必须实现 get_name() 方法！")

    def get_commands(self) -> list[str]:
        """
        【必须实现】返回这个插件能执行的所有命令列表。
        例如: ['create_note', 'edit_note', 'delete_note']
        CommandExecutor 会用这个列表来知道“这个插件会做什么”。
        """
        raise NotImplementedError("每个插件都必须实现 get_commands() 方法！")

    def execute(self, command: str, args: dict, controller) -> None:
        """
        【必须实现】执行具体命令的地方。
        这是插件的核心逻辑，当 CommandExecutor 决定调用你的插件时，
        就会运行这个方法。

        :param command: 要执行的命令名 (e.g., 'create_note')。
        :param args: AI 从用户输入中提取的参数字典 (e.g., {'title': '购物清单'})。
        :param controller: AppController 的实例，让你能访问到其他核心服务，
                           比如通过 controller.view.ui_queue.put(...) 来更新UI。
        """
        raise NotImplementedError("每个插件都必须实现 execute() 方法！")

    def get_spec(self) -> dict:
        """
        【强烈建议实现】返回给 AI 的“插件说明书”，JSON 格式。
        这是实现“智能”的关键！AIService 会读取这个说明，
        才能理解你的插件能做什么、怎么用，以及如何把用户的话翻译成结构化指令。

        如果没有这个，AI就不知道你的插件存在。

        默认实现会尝试在插件目录下寻找一个 `[plugin_name]_prompt.json` 文件并加载它。
        """
        prompt_filename = f"{self.get_name()}_prompt.json"
        plugin_dir = os.path.join(settings.PLUGINS_DIR, self.get_name())
        prompt_path = os.path.join(plugin_dir, prompt_filename)

        if not os.path.exists(prompt_path):
            logger.warning(f"插件 '{self.get_name()}' 缺少说明书: {prompt_path}，AI可能无法调用此插件。")
            return {}

        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载插件 '{self.get_name()}' 的说明书失败: {e}")
            return {}

    def on_load(self):
        """
        【可选实现】当插件被 PluginManager 加载时调用。
        你可以在这里执行一些一次性的初始化操作，比如检查依赖、创建默认配置等。
        """
        # logger.debug(f"插件 '{self.get_name()}' 已加载。")
        pass

    def on_unload(self):
        """
        【可选实现】当插件被 PluginManager 卸载（或重载前）时调用。
        你可以在这里执行一些清理工作，比如关闭文件、断开连接等，防止内存泄漏。
        """
        # logger.debug(f"插件 '{self.get_name()}' 已卸载。")
        pass