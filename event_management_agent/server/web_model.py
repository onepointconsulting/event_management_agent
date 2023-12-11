from pydantic import BaseModel
from typing import Union


class ResponseText(BaseModel):
    response: str
    sources: Union[str, None]


class QuestionAnswer(BaseModel):
    question: str
    answer: str

    def __str__(self):
        return f"""question: {self.question}
answer: {self.answer}"""


if __name__ == "__main__":
    response_text = ResponseText(response="Blah", sources="test")
    print(response_text.model_dump_json())
