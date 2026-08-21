import watcher
from utilities import *
import config
from local_db import createConnection

conn = createConnection()
handler = ChangeHandler()
observer = Observer()
observer.schedule(handler, "/", recursive = True)
while True:
    time.sleep(PERIOD)
    payload = getPayload(conn)
    sendPayload(payload)
    response = receivePayload()
    if response != None:
        newConfig = fetchNewConfig(response)
        config.WATCHED_ROOTS = newConfig.roots
        config.WATCHED_EXTENSIONS = newConfig.extensions
        config.PERIOD = newConfig.period
        maxActionList = payload.generateMaxActionPairList()
        flushActions(conn, maxActionList)
        uploadPathsList = getUploadPathsList(response)
        uploadFiles(uploadPathsList)