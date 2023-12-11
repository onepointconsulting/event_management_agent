import unittest

from event_management_agent.service.event_search_service import combine_history
from event_management_agent.test.web_session_provider import create_dummy_websocket_session


class TestEventSearchService(unittest.TestCase):
    def test_combine_history(self):
        user_prompt = "Show me some events in London."
        session = create_dummy_websocket_session("2")
        combined = combine_history(user_prompt, session)
        assert user_prompt in combined
        assert "question: What is the meaning of life?" in combined
        assert "answer: 42" in combined
