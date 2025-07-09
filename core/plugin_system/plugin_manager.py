# /nana_2/core/plugin_system/plugin_manager.py

import os
import importlib
import sys
from global_config import settings
from core.log.logger_config import logger
from IntentDetector.intent_registry import load_intent_mapping
from plugins.base_plugin import BasePlugin

class PluginManager:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.plugins = {}  # key是插件名, value是插件实例

    def load_all_plugins(self):
        """应用启动时，加载所有插件"""
        logger.info("[插件理] 开始加载所有插件...")
        plugin_folders = [f.name for f in os.scandir(settings.PLUGINS_DIR) if f.is_dir() and not f.name.startswith('_')]
        for plugin_name in plugin_folders:
            self.load_plugin(plugin_name)
        logger.info(f"[插件理] 所有插件加载完毕，共 {len(self.plugins)} 个。")

    def load_plugin(self, plugin_name: str) -> bool:
        """加载单个插件"""
        if plugin_name in self.plugins:
            logger.warning(f"[插件理] 插件 '{plugin_name}' 已经加载了。")
            return True
        try:
            # 动态导入插件模块
            module_path = f"plugins.{plugin_name}"
            if module_path in sys.modules:
                # 如果模块已存在 (比如重载前)，先删掉缓存
                del sys.modules[module_path]

            plugin_module = importlib.import_module(module_path)
            plugin_instance = plugin_module.get_plugin()

            if not isinstance(plugin_instance, BasePlugin):
                raise TypeError(
                    f"插件 '{plugin_name}' 必须继承 BasePlugin"
                )

            # 基本接口检查
            for method in ("get_name", "get_commands", "execute"):
                if not hasattr(plugin_instance, method):
                    raise AttributeError(
                        f"插件 '{plugin_name}' 缺少必要方法 '{method}'"
                    )

            plugin_instance.on_load()  # 调用插件自己的初始化方法
            load_intent_mapping(plugin_name)  # 注册该插件的意图映射
            self.plugins[plugin_name] = plugin_instance
            logger.info(f"[插件理] 成功加载插件: '{plugin_name}'")
            return True
        except Exception as e:
            logger.error(f"[插件理] 加载插件 '{plugin_name}' 失败: {e}", exc_info=True)
            return False

    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载单个插件"""
        if plugin_name not in self.plugins:
            logger.warning(f"[插件理] 尝试卸载一个不存在或未加载的插件: '{plugin_name}'")
            return False
        try:
            plugin_instance = self.plugins[plugin_name]
            plugin_instance.on_unload() # 调用插件自己的清理方法
            del self.plugins[plugin_name]

            # 从sys.modules中移除，确保下次加载是全新的
            module_path = f"plugins.{plugin_name}"
            if module_path in sys.modules:
                del sys.modules[module_path]
                # 注意：其子模块可能需要更复杂的处理，但对我们目前够用

            logger.info(f"[插件理] 成功卸载插件: '{plugin_name}'")
            return True
        except Exception as e:
            logger.error(f"[插件理] 卸载插件 '{plugin_name}' 失败: {e}", exc_info=True)
            return False

    def reload_plugin(self, plugin_name: str) -> tuple[bool, str]:
        """热重载单个插件"""
        logger.info(f"[插件理] 开始热重载插件: '{plugin_name}'...")

        # 1. 先卸载
        if plugin_name in self.plugins:
            if not self.unload_plugin(plugin_name):
                return False, f"重载失败：卸载旧版 '{plugin_name}' 插件时出错。"

        # 2. 再加载
        if self.load_plugin(plugin_name):
            # 3. 通知其他核心服务更新
            self.app_controller.ai_service.rebuild_prompts()
            self.app_controller.command_executor.refresh_commands()
            logger.info(f"[插件理] 插件 '{plugin_name}' 热重载成功！")
            return True, f"插件 '{plugin_name}' 已经成功热重载啦！"
        else:
            return False, f"重载失败：加载新版 '{plugin_name}' 插件时出错。"

    def get_all_specs(self) -> dict:
        """获取所有插件的“说明书”给AI"""
        all_specs = {}
        for name, instance in self.plugins.items():
            all_specs[name] = instance.get_spec()
        return all_specs

    def get_all_commands(self) -> dict:
        """获取所有插件的命令给执行器"""
        all_commands = {}
        for name, instance in self.plugins.items():
            for command in instance.get_commands():
                all_commands[f"{name}.{command}"] = instance

        return all_commands
