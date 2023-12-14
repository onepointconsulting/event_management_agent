import json
from typing import Optional, Tuple, Union, Callable

from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai import AsyncStream

from event_management_agent.config import cfg
from event_management_agent.server.session import (
    WebsocketSession,
)
from event_management_agent.tools.event_search_tool import (
    function_description_search,
    event_search,
)  # Keep event search. Do not remove it
from event_management_agent.log_factory import logger
from event_management_agent.tools.event_url_tool import event_url_request
from event_management_agent.service.event_enhancement_func import (
    extract_event_ids,
    event_enhancement,
)
from event_management_agent.toml_support import prompts


def extract_event_search_parameters(
    user_prompt: str,
    function_call_name: Optional[str] = None,
    function_output: Optional[str] = None,
):
    system_message = prompts["events"]["system_message"]
    assert system_message is not None
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt},
    ]
    kwargs = {"function_call": "auto"}
    if function_call_name is not None and function_output is not None:
        content = function_output
        messages.append(
            {"role": "function", "name": function_call_name, "content": content}
        )
        kwargs = {}
    return messages, kwargs


async def event_search_openai(
    user_prompt: str,
    function_call_name: Optional[str] = None,
    function_output: Optional[str] = None,
    stream: bool = False,
) -> Optional[ChatCompletionMessage]:
    messages, kwargs = extract_event_search_parameters(
        user_prompt, function_call_name, function_output
    )
    completion = await cfg.open_ai_client.chat.completions.create(
        model=cfg.openai_model,
        temperature=cfg.open_ai_temperature,
        messages=messages,
        functions=[function_description_search],
        stream=stream,
        **kwargs,
    )
    if stream:
        return completion
    choices = completion.choices
    if len(choices) > 0:
        return choices[0].message
    else:
        return None


def execute_chat_function(
    chat_completion_message: Optional[ChatCompletionMessage],
) -> Tuple[str, str]:
    if chat_completion_message is None or chat_completion_message.function_call is None:
        return ""
    func_name = chat_completion_message.function_call.name
    func_args = chat_completion_message.function_call.arguments
    if isinstance(func_args, str):
        func_args = json.loads(func_args)
    chosen_func = eval(func_name)
    if "search" not in func_args:
        if "locality" in func_args:
            func_args["search"] = func_args["locality"]
        else:
            func_args["search"] = ""
    return func_name, chosen_func(**func_args)


async def process_search(
    user_prompt: str, session: WebsocketSession, stream: bool
) -> Union[str, AsyncStream]:
    completion_message = await event_search_openai(user_prompt)
    logger.info(completion_message)
    logger.info(type(completion_message))
    if completion_message.function_call is not None:
        logger.info(completion_message.function_call.name)
        logger.info(completion_message.function_call.arguments)
        logger.info(type(completion_message.function_call.arguments))
        func_name, search_json = execute_chat_function(completion_message)

        # Enhancing the events with URL information.
        events_json = json.loads(search_json)
        if "count" not in events_json or events_json["count"] == 0:
            return "Could not find any events"
        event_list = events_json["events"]
        event_ids = extract_event_ids(event_list)
        enhanced_urls = event_url_request(event_ids)
        event_list_with_urls = event_enhancement(event_list, enhanced_urls)
        # Enhancement finished

        logger.info(event_list_with_urls)
        final_completion_message = await event_search_openai(
            combine_history(user_prompt, session),
            func_name,
            event_list_with_urls,
            stream=stream,
        )
        if isinstance(final_completion_message, dict):
            logger.info("")
            logger.info(final_completion_message)
            return final_completion_message.content
        else:
            return final_completion_message


def combine_history(user_prompt: str, session: WebsocketSession) -> str:
    history = session.messages_to_str()
    template = prompts["events"]["combined_message"]
    combined = template.format(history=history, user_prompt=user_prompt)
    logger.info("Combined: %s", combined)
    return combined


async def process_stream(stream: Union[str, AsyncStream], stream_func: Callable):
    async for chunk in stream:
        chunk_message = chunk.choices[0].delta  # extract the message
        if chunk_message.content is not None:
            message_text = chunk_message.content
            stream_func(message_text)


async def aprocess_stream(
    stream: Union[str, AsyncStream], stream_func: Callable, session: WebsocketSession
):
    if stream is None:
        await stream_func("Sorry, I could not find any events")
    elif isinstance(stream, str):
        await stream_func(stream)
    else:
        async for chunk in stream:
            if session.stop_stream:
                break
            if not isinstance(chunk, str):
                chunk_message = chunk.choices[0].delta  # extract the message
                if chunk_message.content is not None:
                    message_text = chunk_message.content
                    await stream_func(message_text)
            else:
                logger.info("Chunk as string: %s", chunk)
                await stream_func(chunk)


if __name__ == "__main__":
    import asyncio

    async def process_experiment(user_prompt):
        search_result = await process_search(user_prompt, True)
        if isinstance(search_result, str):
            logger.info(search_result)
        else:
            await process_stream(
                search_result, lambda message: print(f"{message}", end="")
            )

    # process_experiment("Can you give all health related events in London?")
    # process_experiment("Can you give all events about positive thinking in London?")
    asyncio.run(
        process_experiment(
            "Can you give all health related events in the United Kingdom?"
        )
    )
    # process_experiment("I am interested in events about women.")
