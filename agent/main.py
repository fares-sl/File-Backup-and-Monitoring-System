from watcher import ChangeHandler, ConfigurateWatchers 
from watchdog.observers import Observer
from utilities import getPayload, sendPayload, uploadFiles, registerWithServer
import config
from local_db import createConnection, flushActions, getAgentId, saveAgentId
import time


conn = createConnection(config.AGENT_DB)
agent_id = getAgentId(conn)
if agent_id is None:
    agent_id = registerWithServer()
    if agent_id is None:
        print("Could not register agent with server.")
        conn.close()
        raise SystemExit(1)
    saveAgentId(conn, agent_id)
print(f'agent id: {agent_id}')
handler = ChangeHandler()
observer = Observer()
watchers = {}
ConfigurateWatchers(observer, handler, watchers, config.WATCHED_ROOTS)
observer.start()
while True:
    time.sleep(config.PERIOD)
    payload = getPayload(conn, agent_id)
    respond = sendPayload(payload)
    if respond is not None:
        config.WATCHED_ROOTS = respond['roots']
        ConfigurateWatchers(observer, handler, watchers, config.WATCHED_ROOTS)
        config.WATCHED_EXTENSIONS = respond['extensions']
        config.PERIOD = respond['period']
        if not payload.noAction():
            maxActionId = payload.getMaxActionId()
            flushActions(conn, maxActionId)
            uploadFiles(respond['paths'], agent_id)