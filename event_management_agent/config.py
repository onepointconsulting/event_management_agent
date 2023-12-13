import os

from pathlib import Path
from dotenv import load_dotenv
from event_management_agent.log_factory import logger
from openai import AsyncOpenAI


load_dotenv()


def create_if_not_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


class Config:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key is not None
    open_ai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0."))
    openai_model = os.getenv("OPENAI_MODEL")
    assert openai_model is not None
    open_ai_client = AsyncOpenAI(
        api_key=openai_api_key,
    )

    websocket_server = os.getenv("WEBSOCKET_SERVER")
    assert websocket_server is not None
    websocket_port = int(os.getenv("WEBSOCKET_PORT"))
    websocket_cors_allowed_origins = os.getenv("WEBSOCKET_CORS_ALLOWED_ORIGINS", "*")

    project_root = Path(os.getenv("PROJECT_ROOT"))
    assert project_root.exists()
    include_description = os.getenv("INCLUDE_DESCRIPTION")
    assert include_description in ["true", "false"]

    history_size = int(os.getenv("HISTORY_SIZE"))
    history_token_limit = int(os.getenv("HISTORY_TOKEN_LIMIT"))

    search_results_size = int(os.getenv("SEARCH_RESULTS_SIZE"))

    # UI Related
    ui_folder = Path(os.getenv("UI_FOLDER"))
    create_if_not_exists(ui_folder)

    def __repr__(self) -> str:
        return f"""

OPENAI_API_KEY=sk-{self.openai_api_key}
OPENAI_TEMPERATURE={self.open_ai_temperature}
OPENAI_MODEL={self.openai_model}
"""


cfg = Config()


if __name__ == "__main__":
    logger.info(cfg)
