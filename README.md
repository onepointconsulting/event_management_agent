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

Please make sure to install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) first.

```
conda create -n event_management_agent python=3.12
conda activate event_management_agent
pip install poetry
poetry install
```

## Configuration

The application can be configured via a `.env` file. The easiest way to start is to copy the `.env_local` to `,env` and replace the missing variables.

!Warning!: if you get an error regarding frozenlist compilation problems on Windows, please download Microsoft Visual C++ 14.0 or greater from https://visualstudio.microsoft.com/visual-cpp-build-tools/

## Running the application

Change directory to the root folder of the project and run:

```
python .\event_management_agent\server\websocket_server.py
```

## Running unit tests

```
python -m unittest
```