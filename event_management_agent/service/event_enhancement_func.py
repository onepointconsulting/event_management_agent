from typing import List
import json


def event_enhancement(events_list: List[str], urls: str) -> str:
    urls_list = json.loads(urls)
    url_map = {event["id"]: event for event in urls_list}
    for event in events_list:
        url_info = url_map.get(event["id"])
        if url_info is not None:
            event["url"] = url_info["url"]
    return json.dumps(events_list)


def extract_event_ids(events_list: List[dict]) -> List[int]:
    return [event["id"] for event in events_list]


if __name__ == "__main__":
    from event_management_agent.log_factory import logger

    events_str = """{"count":3,"total":3,"events":[{"id":4584199,"eventDateId":4584204,"name":"Special Event - Women and Spirituality - (Langley) First Tuesday of Every Month  ","subTitle":"","speakerName":"","speakerDescription":"","requiresRegistration":false,"startDate":"2023-12-05","startTime":"13:00","endDate":"2023-12-05","endTime":"15:00","venueName":"Slough Langley St. Mary\'s Church Hall, ","locality":"Slough","postalCode":"SL3 7ER","countryName":"united kingdom","venueAddress":"St. Mary\'s Church Hall, \\n2 St Mary’s Road, \\nLangley, \\n","longitude":0.0,"eventTypeId":13,"eventName":"Special Event - Women and Spirituality - (Langley) First Tuesday of Every Month  "},{"id":4068259,"eventDateId":4639443,"name":"Women Inspired","subTitle":"Monthly Talk And Discussion","speakerName":"","speakerDescription":"","requiresRegistration":false,"startDate":"2023-12-09","startTime":"14:30","endDate":"2023-12-09","endTime":"15:45","venueName":"Global Co-operation House  ","locality":"London","postalCode":"NW10 2HH","countryName":"united kingdom","venueAddress":"65-69 Pound Lane, Willesden Green","longitude":0.0,"eventTypeId":8,"eventName":"Women Inspired"},{"id":4068259,"eventDateId":4663780,"name":"Women Inspired","subTitle":"Monthly Talk And Discussion","speakerName":"","speakerDescription":"","requiresRegistration":false,"startDate":"2024-01-13","startTime":"14:30","endDate":"2024-01-13","endTime":"15:45","venueName":"Global Co-operation House  ","locality":"London","postalCode":"NW10 2HH","countryName":"united kingdom","venueAddress":"65-69 Pound Lane, Willesden Green","longitude":0.0,"eventTypeId":8,"eventName":"Women Inspired"}]}"""
    urls = """[{"url_template":"https://brahmakumaris.uk/event/?id=@eventId@","url":"https://brahmakumaris.uk/event/?id=11111","id":11111},{"url_template":"https://globalcooperationhouse.org/whatson-full/singleevent/@eventId@","url":"https://globalcooperationhouse.org/whatson-full/singleevent/4256334","id":4256334}]"""
    event_list = json.loads(events_str)
    event_list = event_list["events"]
    enhanced_list = event_enhancement(event_list, urls)
    assert enhanced_list is not None
    logger.info(enhanced_list)
    logger.info(extract_event_ids(event_list))


