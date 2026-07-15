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

    def test_parse_transaction_returns_dict(self):
        parsed = self.agent.parse_transaction('Log transaction: HCP John Doe, Meeting, topics: Product X, attendees: Rep, outcomes: Positive response')
        self.assertIsInstance(parsed, dict)


if __name__ == '__main__':
    unittest.main()
