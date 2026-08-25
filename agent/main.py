from watcher import ChangeHandler, ConfigurateWatchers 
from watchdog.observers import Observer
from utilities import getPayload, sendPayload, uploadFiles
import config
from local_db import createConnection, flushActions
import time
from classes import Payload


conn = createConnection(config.AGENT_DB)
handler = ChangeHandler()
observer = Observer()
watchers = {}
ConfigurateWatchers(observer, handler, watchers, config.WATCHED_ROOTS)
observer.start()
while True:
    time.sleep(config.PERIOD)
    payload = getPayload(conn)
    respond = sendPayload(payload)
    if respond != None:
        config.WATCHED_ROOTS = respond['roots']
        ConfigurateWatchers(observer, handler, watchers, config.WATCHED_ROOTS)
        config.WATCHED_EXTENSIONS = respond['extensions']
        config.PERIOD = respond['period']
        if not payload.noAction():
            maxActionId = payload.getMaxActionId()
            flushActions(conn, maxActionId)
            uploadFiles(respond['paths'])