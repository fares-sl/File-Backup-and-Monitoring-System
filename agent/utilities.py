import local_db
import classes
import socket
import json
import requests
from datetime import datetime
import getpass

def fetchActionList(cur):
    actionList = []
    action = cur.fetchone()
    if action is None :
        return actionList
    pathActions = PathActions(action[0], action[2] - 1)
    actionList.append(pathActions)
    actionList[-1].appendAction(action[1], action[3], action[4])
    for action in cur:
        if action[0] != actionList[-1].pathName :
            pathActions = PathActions(action[0], action[2] - 1)
            actionList.append(pathActions)
        actionList[-1].appendAction(action[1], action[3], action[4])
    return actionList


def getPayload(conn):
    cur = getActions(conn)
    hostName = socket.gethostname()
    payload = Payload(hostName, fetchActionList(cur))
    return payload

def sendPayload(payload):
    url = f"http://{config.SERVER_IP}:{config.SERVER_PORT}{config.ENDPOINT}"

   try:
        response = requests.post(
            url,
            json=payload.to_dict(),
            timeout=config.TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        print("Server took too long to respond")
        return None

    except requests.exceptions.ConnectionError:
        print("Could not connect to server")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"Server returned an HTTP error: {e}")
        return None

def getTime():
     return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getUser():
    return getpass.getuser()