from typing import List

from event_management_agent.tools.request_processing_func import (
    process_request,
    process_event_ids_request,
)
from event_management_agent.log_factory import logger


def single_event(event_ids: List[int]) -> str:
    if len(event_ids) == 0:
        return "No event id specified"
    return process_event_ids_request(
        "https://events.brahmakumaris.org/bkregistration/organisationEventReportController.do?simpleEventTemplate=jsonEvent.ftl&mimeType=application/json&eventIds={event_ids_str}",
        event_ids,
        "Cannot fetch data for single events",
    )


function_description_single_event = {
    "name": "single_event",
    "description": "Provides detailed information about events based on multiple event identifiers or event ids",
    "type": "object",
    "parameters": {
        "type": "object",
        "properties": {
            "event_ids": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "An optional list of event ids, like e.g. 345345, 432134",
            },
        },
        "required": ["event_ids"],
    },
}


if __name__ == "__main__":
    from event_management_agent.tools.event_search_tool import event_search
    import json

    res = event_search("London", None, [])
    events_json = json.loads(res)
    if "events" in events_json:
        first_event = events_json["events"][0]
        event_id = first_event["id"]
        if event_id > 0:
            event_details = single_event([event_id])
            assert event_details is not None
            logger.info(event_details)
