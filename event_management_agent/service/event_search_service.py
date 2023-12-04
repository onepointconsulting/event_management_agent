import json
from typing import Optional, Tuple

from openai.types.chat.chat_completion_message import ChatCompletionMessage


from event_management_agent.config import cfg
from event_management_agent.tools.event_search_tool import (
    function_description_search,
    event_search,
)  # Keep event search. Do not remove it
from event_management_agent.tools.single_event_tool import (
    function_description_single_event,
)
from event_management_agent.tools.event_url_tool import event_url_request
from event_management_agent.service.event_enhancement_func import extract_event_ids, event_enhancement


def event_search_openai(
    user_prompt: str,
    function_call_name: Optional[str] = None,
    function_output: Optional[str] = None,
) -> Optional[ChatCompletionMessage]:
    messages = [{"role": "user", "content": user_prompt}]
    kwargs = {"function_call": "auto"}
    if function_call_name is not None and function_output is not None:
        content = function_output
        messages.append(
            {"role": "function", "name": function_call_name, "content": content}
        )
        kwargs = {}
    completion = cfg.open_ai_client.chat.completions.create(
        model=cfg.openai_model,
        temperature=cfg.open_ai_temperature,
        messages=messages,
        functions=[function_description_search, function_description_single_event],
        **kwargs
    )
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
    return func_name, chosen_func(**func_args)


def process_search(user_prompt: str) -> str:
    completion_message = event_search_openai(user_prompt)
    logger.info(completion_message)
    logger.info(type(completion_message))
    if completion_message.function_call is not None:
        logger.info(completion_message.function_call.name)
        logger.info(completion_message.function_call.arguments)
        logger.info(type(completion_message.function_call.arguments))
        func_name, search_json = execute_chat_function(completion_message)

        # Enhancing the events with URL information.
        events_json = json.loads(search_json)
        if events_json['count'] == 0:
            return "Could not find any events"
        event_list = events_json["events"]
        event_ids = extract_event_ids(event_list)
        enhanced_urls = event_url_request(event_ids)
        event_list_with_urls = event_enhancement(event_list, enhanced_urls)
        # Enhancement finished

        logger.info(event_list_with_urls)
        final_completion_message = event_search_openai(
            user_prompt, func_name, event_list_with_urls
        )
        logger.info("")
        logger.info(final_completion_message)
        return final_completion_message.content


if __name__ == "__main__":
    from event_management_agent.log_factory import logger

    def process_experiment(user_prompt):
        search_result = process_search(user_prompt)
        logger.info(search_result)

    # user_prompt = "Can you give all health related events in London?"
    # search_result = process_search(user_prompt)
    # logger.info(search_result)

    # user_prompt = "Can you give all events about positive thinking in London?"
    # search_result = process_search(user_prompt)
    # logger.info(search_result)

    # user_prompt = "Can you give all health related events in the United Kingdom?"
    # search_result = process_search(user_prompt)
    # logger.info(search_result)

    process_experiment("Can you give all health related events in London?")
    process_experiment("Can you give all events about positive thinking in London?")
    process_experiment("Can you give all health related events in the United Kingdom?")
    process_experiment("I am interested in events about women.")
    
    
