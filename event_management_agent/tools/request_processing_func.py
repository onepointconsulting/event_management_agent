import requests

from typing import List

from event_management_agent.log_factory import logger


def process_request(url: str, operation_name: str) -> str:
    try:
        res = requests.get(url)
        return res.content.decode("utf-8")
    except Exception as e:
        err_message = f"Failed {operation_name} due to {e}"
        logger.exception(err_message)
        return err_message


def process_event_ids_request(
    url_template: str, event_ids: List[int], failure_message: str
):
    event_ids_str = ",".join([str(i) for i in event_ids])
    url = url_template.format(event_ids_str=event_ids_str)
    return process_request(url, failure_message)
