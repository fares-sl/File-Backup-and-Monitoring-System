import watcher.py
import time

def getPayload(conn):
    cur = getActions(conn)
    

conn = createConnection()
handler = ChangeHandler()
observer = Observer()
observer.schedule(handler, "/", recursive = True)
while True:
    time.sleep(period)
    payload = getPayload(conn)
    sendPayload(payload)
    respnse = receivePayload()
    if respnse:
        maxActionList = generateMaxActionPairList(payload)
        flushActions(conn, maxActionList)
        uploadPathsList = getUploadPathsList(respnse)
        uploadFiles(uploadPathsList)