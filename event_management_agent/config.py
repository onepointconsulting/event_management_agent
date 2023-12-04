import os
from dotenv import load_dotenv
from event_management_agent.log_factory import logger
from openai import OpenAI


load_dotenv()


class Config:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key is not None
    open_ai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0."))
    openai_model = os.getenv("OPENAI_MODEL")
    assert openai_model is not None
    open_ai_client = OpenAI(
        api_key=openai_api_key,
    )

    def __repr__(self) -> str:
        return f"""

OPENAI_API_KEY=sk-{self.openai_api_key}
OPENAI_TEMPERATURE={self.open_ai_temperature}
OPENAI_MODEL={self.openai_model}
"""


cfg = Config()


if __name__ == "__main__":
    logger.info(cfg)
