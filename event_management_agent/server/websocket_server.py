import socketio
from aiohttp import web
from event_management_agent.server.session import get_session

from event_management_agent.log_factory import logger
from event_management_agent.config import cfg
from event_management_agent.server.web_model import ResponseText
from event_management_agent.service.event_search_service import (
    process_search,
    aprocess_stream,
)

sio = socketio.AsyncServer(cors_allowed_origins=cfg.websocket_cors_allowed_origins)
app = web.Application()
sio.attach(app)


@sio.event
def connect(sid, environ):
    logger.info("connect %s ", sid)


async def send_simple_message(message: str, sid: str):
    response_text = ResponseText(response=message, sources=None)
    await sio.emit("response", response_text.model_dump_json(), room=sid)


@sio.event
async def question(sid: str, data: str):
    logger.info("question (%s): %s", sid, data)
    session = get_session(sid)
    session.add_question(data)

    async def stream_to_client(message: str):
        print(f"{message}", end="")
        session.append_to_answer(message)
        await send_simple_message(message, sid)

    try:
        search_result = await process_search(data, session, True)
        await aprocess_stream(search_result, stream_to_client)
    except:
        logger.exception(f"Failed to process {data}")
        await send_simple_message("Failed to process request. Please try again.", sid)

    session.add_message()
    await sio.emit("stopstreaming", room=sid)


@sio.event
def disconnect(sid):
    logger.info("disconnect %s", sid)


if __name__ == "__main__":
    web.run_app(app, host=cfg.websocket_server, port=cfg.websocket_port)
