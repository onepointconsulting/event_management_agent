import urllib.parse

from typing import Optional, List
from event_management_agent.tools.request_processing_func import process_request
from event_management_agent.log_factory import logger
from event_management_agent.config import cfg


def event_search(
    search: str,
    locality: Optional[str] = "",
    country: Optional[str] = "",
    tags: List[str] = [],
) -> str:
    offset: int = 0
    limit: int = 20
    country_filter = (
        f"filterByCountry={urllib.parse.quote_plus(country.capitalize())}"
        if country is not None and len(country) > 0
        else ""
    )
    tags_param = f"&tags={", ".join(tags)}" if len(tags) > 0 else ""
    if locality is not None and len(locality) > 0:
        search = f"{search} AND {locality}"
    url = f"https://events.brahmakumaris.org/events-rest/event-search-v2?search={urllib.parse.quote_plus(search)}&limit={limit}&offset={offset}&{country_filter}{tags_param}&includeDescription={cfg.include_description}"
    logger.info("Calling %s", url)
    return process_request(url, f"search for {search}")


function_description_search = {
    "name": "event_search",
    "description": "Searches for events either by location, like city name, e.g: London or by topic, like e.g. 'yoga'. It also allows to set a filter by country and filteer by tags",
    "type": "object",
    "parameters": {
        "type": "object",
        "properties": {
            "search": {
                "type": "string",
                "description": "The search string which can include topics like e.g: 'meditation', 'women' or it can also include names of places like 'Worthing'",
            },
            "locality": {
                "type": "string",
                "description": "The name of a locality, like e.g: 'Dublin', 'Lisbon', 'Manchester', 'Lisboa'",
            },
            "country": {
                "type": "string",
                "description": "The name of a country, like e.g: 'Ireland'",
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "An optional list of tags, like 'retreat'",
            },
        },
        "required": ["search"],
    },
}


if __name__ == "__main__":
    res = event_search("London", None, [])
    logger.info(res)
