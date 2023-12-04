# Event Management Agent

Simple agent which demonstrates how you can create conversational agents on top of some sinple REST interfaces.

These are the interfaces:

#### Events by keyword and country
GET https://events.brahmakumaris.org/events-rest/event-search-v2?search=positive&limit=20&offset=0&filterByCountry=United%20Kingdom&includeDescription=true

GET https://events.brahmakumaris.org/events-rest/event-search-v2?search=positive%20%20London&limit=20&offset=0&filterByCountry=United%20Kingdom&includeDescription=true

GET https://events.brahmakumaris.org/events-rest/event-search-v2?search=positive&limit=10&offset=0

#### Single Event Detail
GET https://events.brahmakumaris.org/bkregistration/organisationEventReportController.do?simpleEventTemplate=jsonEvent.ftl&mimeType=text/plain&eventIds=4256334,4256334

#### Fetch Event URLs
GET https://events.brahmakumaris.org/bkregistration/events?eventIds=4256334,5678

## Installation instructions

```
conda create -n event_management_agent python=3.12
conda activate event_management_agent
pip install poetry
poetry install
```