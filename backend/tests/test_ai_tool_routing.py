import unittest

from app.langgraph_agent import LangGraphAgent


class AIChatRoutingTests(unittest.TestCase):
    def setUp(self):
        self.agent = LangGraphAgent()

    def test_log_transaction_prompt_routes_to_log_interaction(self):
        tool = self.agent.route_tool('Please log this transaction in the AI chatbot')
        self.assertEqual(tool, 'Log Interaction')

    def test_summarize_prompt_routes_to_summarize_interaction(self):
        tool = self.agent.route_tool('Please summarize this interaction')
        self.assertEqual(tool, 'Summarize Interaction')


if __name__ == '__main__':
    unittest.main()
