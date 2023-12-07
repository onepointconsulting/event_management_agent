from pydantic import BaseModel
from typing import Union

class ResponseText(BaseModel):
    response: str
    sources: Union[str, None]


if __name__ == "__main__":
    response_text = ResponseText(response="Blah", sources="test")
    print(response_text.model_dump_json())