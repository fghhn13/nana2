import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from global_config import settings

class ClarificationPromptTest(unittest.TestCase):
    def test_prompt_contains_clarification_intent(self):
        with open(settings.PROMPTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        examples = data['command_recognizer']['examples']
        intents = [ex.get('ai', {}).get('intent') for ex in examples]
        self.assertIn('needs_clarification', intents)

if __name__ == '__main__':
    unittest.main()
