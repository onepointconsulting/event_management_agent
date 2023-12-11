from typing import Dict, List, Union

from event_management_agent.server.web_model import (
    QuestionAnswer,
)
from event_management_agent.config import cfg

class WebsocketSession:
    def __init__(
        self,
        # Id from the session cookie
        socket_id: str,
        message_limit: int = cfg.history_size,
    ):
        self.socket_id = socket_id
        self.current_question = ""
        self.current_answer = ""
        self.messages: List[QuestionAnswer] = []
        self.cancel_message: bool = False
        self.message_limit = message_limit
        ws_sessions_sid[socket_id] = self

    def add_message(self):
        question_answer = QuestionAnswer(
            question=self.current_question, answer=self.current_answer
        )
        self.messages.append(question_answer)
        if len(self.messages) > self.message_limit:
            self.messages.pop(0)
        self.current_question = ""
        self.current_answer = ""

    def add_question(self, current_question: str):
        self.current_question = current_question

    def append_to_answer(self, current_answer: str):
        self.current_answer += current_answer

    def messages_to_str(self):
        messages = [str(m) for m in self.messages]
        return "\n\n".join(messages)


def get_session(socket_id: str) -> WebsocketSession:
    session: Union[WebsocketSession, None] = ws_sessions_sid.get(socket_id)
    if session is None:
        return WebsocketSession(socket_id)
    return session


ws_sessions_sid: Dict[str, WebsocketSession] = {}
