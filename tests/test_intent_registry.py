import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.plugin_system.plugin_manager import PluginManager
from IntentDetector.intent_registry import intent_registry

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

class IntentRegistryTest(unittest.TestCase):
    def test_mapping_loaded(self):
        controller = DummyController()
        manager = PluginManager(controller)
        manager.load_plugin('note_taker')
        self.assertIn('create', intent_registry)
        self.assertEqual(intent_registry['create'], ('note_taker', 'create_note'))
        self.assertIn('clarify_action', intent_registry)
        self.assertEqual(intent_registry['clarify_action'], ('note_taker', 'read_note'))
        self.assertIn('search_notes_by_keyword', intent_registry)
        self.assertEqual(
            intent_registry['search_notes_by_keyword'],
            ('note_taker', 'search_notes')
        )

if __name__ == '__main__':
    unittest.main()
