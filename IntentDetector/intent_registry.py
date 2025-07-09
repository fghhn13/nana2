import os
import json
from global_config import settings
from core.log.logger_config import logger

intent_registry: dict[str, tuple[str, str]] = {}


def register_intent(intent: str, plugin: str, command: str):
    """注册单个意图映射到对应的插件和命令"""
    intent_registry[intent] = (plugin, command)


def load_intent_mapping(plugin_name: str):
    """从指定插件目录加载 intent 映射文件"""
    mapping_path = os.path.join(settings.PLUGINS_DIR, plugin_name, "intent_map.json")
    if not os.path.exists(mapping_path):
        return
    try:
        with open(mapping_path, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        for intent, target in mapping.items():
            if isinstance(target, str):
                if "." in target:
                    plugin, command = target.split(".", 1)
                else:
                    plugin, command = plugin_name, target
                register_intent(intent, plugin, command)
            elif isinstance(target, dict):
                plugin = target.get("plugin", plugin_name)
                command = target.get("command")
                if command:
                    register_intent(intent, plugin, command)
    except Exception as e:
        logger.error(f"[意图映射] 加载 {mapping_path} 失败: {e}")


def get_mapping(intent: str):
    """根据意图名称获取 (plugin, command)"""
    return intent_registry.get(intent)

