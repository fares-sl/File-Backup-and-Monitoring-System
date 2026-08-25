from local_db import getActions
from classes import Payload
import socket
import requests
from datetime import datetime
import getpass
import config
from pathlib import Path


def getPayload(conn):
    cur = getActions(conn)
    hostName = socket.gethostname()
    payload = Payload(hostName, cur.fetchall())
    return payload

def sendPayload(payload):
    url = f"http://{config.SERVER_IP}:{config.SERVER_PORT}{config.ENDPOINT}"

    try:
        response = requests.post(
            url,
            json=payload.__dict__,
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

def extension(filePath):
    return Path(filePath).suffix

def uploadFiles(paths):
    print(f"paths to upload are {paths}")