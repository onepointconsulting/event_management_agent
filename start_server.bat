REM Simple script that can be used to start the application.
cd /D "%~dp0"
call conda activate event_management_agent
call python .\event_management_agent\server\websocket_server.py