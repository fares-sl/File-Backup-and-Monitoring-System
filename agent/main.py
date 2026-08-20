import watcher
import time
import utilities
import config

conn = createConnection()
handler = ChangeHandler()
observer = Observer()
observer.schedule(handler, "/", recursive = True)
while True:
    time.sleep(period)
    payload = getPayload(conn)
    sendPayload(payload)
    respnse = receivePayload()
    if respnse != None:
        newConfig = fetchNewConfig(response)
        updateConfig(newConfig, WATCHED_ROOTS, WATCHED_EXTENSIONS)
        maxActionList = payload.generateMaxActionPairList()
        flushActions(conn, maxActionList)
        uploadPathsList = getUploadPathsList(respnse)
        uploadFiles(uploadPathsList)