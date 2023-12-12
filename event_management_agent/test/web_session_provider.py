from event_management_agent.server.session import get_session


def create_dummy_websocket_session(session_id="1"):
    session = get_session(session_id)
    assert session.socket_id == session_id
    question = "What is the meaning of life?"
    session.add_question(question)
    session.append_to_answer("4")
    session.append_to_answer("2")
    assert session.current_answer == "42"
    assert session.current_question == question
    session.add_message()
    return session
