import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.plugin_system.plugin_manager import PluginManager


class DummyAIService:
    def rebuild_prompts(self):
        pass


class DummyCommandExecutor:
    def refresh_commands(self):
        pass


class DummyController:
    def __init__(self):
        self.ai_service = DummyAIService()
        self.command_executor = DummyCommandExecutor()


class PluginManagerUtilityTests(unittest.TestCase):
    def setUp(self):
        self.controller = DummyController()
        self.manager = PluginManager(self.controller)
        self.plugin_name = "test_plugin"
        module_path = f"plugins.{self.plugin_name}"
        if module_path in sys.modules:
            del sys.modules[module_path]
        self.manager.load_plugin(self.plugin_name)

    def tearDown(self):
        module_path = f"plugins.{self.plugin_name}"
        if self.plugin_name in self.manager.plugins:
            self.manager.unload_plugin(self.plugin_name)
        elif module_path in sys.modules:
            del sys.modules[module_path]

    def test_get_all_commands(self):
        commands = self.manager.get_all_commands()
        self.assertIn("test_plugin.echo", commands)
        self.assertIs(commands["test_plugin.echo"], self.manager.plugins[self.plugin_name])

    def test_get_all_specs(self):
        specs = self.manager.get_all_specs()
        self.assertIn(self.plugin_name, specs)
        self.assertEqual(specs[self.plugin_name], {})

    def test_unload_plugin(self):
        module_path = f"plugins.{self.plugin_name}"
        self.assertIn(self.plugin_name, self.manager.plugins)
        self.assertIn(module_path, sys.modules)
        result = self.manager.unload_plugin(self.plugin_name)
        self.assertTrue(result)
        self.assertNotIn(self.plugin_name, self.manager.plugins)
        self.assertNotIn(module_path, sys.modules)


if __name__ == "__main__":
    unittest.main()
