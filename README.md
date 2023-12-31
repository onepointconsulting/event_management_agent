# Event Management Agent

Simple agent which demonstrates how you can create conversational agents on top of some sinple REST interfaces.

These are the interfaces:

#### Events Search by keyword and country

Examples:

GET https://events.brahmakumaris.org/events-rest/event-search-v2?search=positive&limit=20&offset=0&filterByCountry=United%20Kingdom&includeDescription=true

GET https://events.brahmakumaris.org/events-rest/event-search-v2?search=positive%20%20London&limit=20&offset=0&filterByCountry=United%20Kingdom&includeDescription=true

GET https://events.brahmakumaris.org/events-rest/event-search-v2?search=positive&limit=10&offset=0

#### Enrichment interface

Example:

GET https://events.brahmakumaris.org/bkregistration/events/urls?eventIds=47944,4256334,5678,4654963,4570348

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
python ./event_management_agent/server/websocket_server.py
```

## Running unit tests

```
python -m unittest
```

### Notice about problems with MIME Types whilst service Javascript files

If your Js files are being served by our script `websocket_server.py` under Windows 10 or 11 and you get an error like:

`Expected a JavaScript module script but the server responded with a MIME type of "text/plain"`

Please open `regedit.exe` on Windows and edit the Content-Type value for this key: `HKEY_CLASSES_ROOT\.js` to `application/javascript`.