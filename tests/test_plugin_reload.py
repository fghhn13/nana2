import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.plugin_system.plugin_manager import PluginManager

class DummyAIService:
    def __init__(self):
        self.called = False
    def rebuild_prompts(self):
        self.called = True

class DummyCommandExecutor:
    def __init__(self):
        self.called = False
    def refresh_commands(self):
        self.called = True

class DummyController:
    def __init__(self):
        self.ai_service = DummyAIService()
        self.command_executor = DummyCommandExecutor()

class PluginReloadTests(unittest.TestCase):
    def test_reload(self):
        controller = DummyController()
        manager = PluginManager(controller)
        # ensure plugin loads
        self.assertTrue(manager.load_plugin('sample_plugin'))
        self.assertIn('sample_plugin', manager.plugins)
        # reload
        success, _ = manager.reload_plugin('sample_plugin')
        self.assertTrue(success)
        self.assertTrue(controller.ai_service.called)
        self.assertTrue(controller.command_executor.called)

if __name__ == '__main__':
    unittest.main()
