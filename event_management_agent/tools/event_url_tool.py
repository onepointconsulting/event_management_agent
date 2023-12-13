from typing import List
from event_management_agent.tools.request_processing_func import (
    process_event_ids_request,
)


def event_url_request(event_ids: List[int]) -> str:
    if len(event_ids) == 0:
        return {}
    return process_event_ids_request(
        "https://events.brahmakumaris.org/bkregistration/events/urls?eventIds={event_ids_str}",
        event_ids,
        "Cannot fetch data for single events",
    )


if __name__ == "__main__":
    from event_management_agent.log_factory import logger

    response = event_url_request([4256334, 11111])
    logger.info(response)
    logger.info(type(response))
