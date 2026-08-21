import watcher
import utilities
import config

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
        WATCHED_ROOTS = newConfig.roots
        WATCHED_EXTENSIONS = newConfig.extensions
        PERIOD = newConfig.period
        maxActionList = payload.generateMaxActionPairList()
        flushActions(conn, maxActionList)
        uploadPathsList = getUploadPathsList(response)
        uploadFiles(uploadPathsList)