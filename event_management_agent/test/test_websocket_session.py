import unittest

from event_management_agent.server.session import get_session
from event_management_agent.test.web_session_provider import (
    create_dummy_websocket_session,
)


class TestWebsocketSession(unittest.TestCase):
    def test_add_message(self):
        session = create_dummy_websocket_session("1")
        assert len(session.messages) == 1


if __name__ == "__main__":
    unittest.main()
