import tiktoken

from event_management_agent.config import cfg


def num_tokens_from_string(string: str, model_name: str) -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def num_tokens_from_string_configured(string: str) -> int:
    return num_tokens_from_string(string, cfg.openai_model)


if __name__ == "__main__":
    print(num_tokens_from_string_configured("Hello, world"))
