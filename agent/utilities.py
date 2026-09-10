from local_db import getActions, addNewUser, addRoot, addExtension, getRoots, getExtensions, getPeriod, deleteExtensions,  deleteRoots, modifyPeriod
from classes import Payload, getActionsList
import socket
import requests
from datetime import datetime
import getpass
import config
from pathlib import Path
import psutil
import platform



def getPayload(conn, device_id, user):
    cur = getActions(conn, user)
    hostName = socket.gethostname()
    payload = Payload(user, device_id, getActionsList(cur.fetchall()))
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

def extension(filePath):
    return Path(filePath).suffix

def uploadFiles(paths, device_id):
    for path in paths:
        try:
            with open(path, 'rb') as file:
                response = requests.post(
                    f"http://{config.SERVER_IP}:{config.SERVER_PORT}{config.UPLOAD_ENDPOINT}",
                    files = {'file' : file},
                    data = {
                        'device_id' : device_id,
                        'path' : path,
                    },
                    timeout = config.TIMEOUT
                )
            response.raise_for_status()
            print(f"Uploaded: {path}")
        except Exception as e:
            print(f"Failed to upload {path}: {e}")


def get_physical_mac_addresses() -> list:
    mac_list = []
    virtual_keywords = {
        'virtual', 'vmnet', 'vboxnet', 'docker', 'veth', 'lo', 
        'loopback', 'wsl', 'teredo', 'isatap', 'vpn', 'zerotier'
    }
    
    if_addresses = psutil.net_if_addrs()
    
    for interface_name, addrs in if_addresses.items():
        name_lower = interface_name.lower()
        if any(keyword in name_lower for keyword in virtual_keywords):
            continue
            
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac = addr.address
                if mac and mac != '00:00:00:00:00:00':
                    formatted_mac = mac.replace('-', ':').upper()
                    if formatted_mac not in mac_list:
                        mac_list.append(formatted_mac)
                        
    return mac_list



def registerWithServer():
    hostName = socket.gethostname()
    url = f"http://{config.SERVER_IP}:{config.SERVER_PORT}{config.REGISTER_ENDPOINT}"
    jsonObject = {'hostName': hostName, 'platform': platform.system(), 'mac': get_physical_mac_addresses()}
    try:
        response = requests.post(
            url,
            json=jsonObject,
            timeout=config.TIMEOUT
        )

        response.raise_for_status()

        return response.json()['device_id']

    except requests.exceptions.Timeout:
        print("Server took too long to respond")
        return None

    except requests.exceptions.ConnectionError:
        print("Could not connect to server")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"Server returned an HTTP error: {e}")
        return None

def getDefaultWatchedRoot():
    default_root = Path.home() / 'FIM_WATCH'
    default_root.mkdir(
        parents = True,
        exist_ok = True
    )
    return str(default_root)

def registerUser(user, device_id):
    url = f"http://{config.SERVER_IP}:{config.SERVER_PORT}{config.REGISTER_USER_ENDPOINT}"
    jsonObject = {'device_id':device_id , 'user': user, 'watched_roots': config.WATCHED_ROOTS, 'watched_extensions': config.WATCHED_EXTENSIONS, 'period': config.PERIOD}
    try:
        response = requests.post(
            url,
            json=jsonObject,
            timeout=config.TIMEOUT
        )

        response.raise_for_status()

        return response

    except requests.exceptions.Timeout:
        print("Server took too long to respond")
        return None

    except requests.exceptions.ConnectionError:
        print("Could not connect to server")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"Server returned an HTTP error: {e}")
        return None

def addUser(conn, user , watchedRoots, watchedExtensions, period):
    addNewUser(conn, user, period)
    for root in watchedRoots:
        addRoot(conn, user, root)
    for extension in watchedExtensions:
        addExtension(conn, user, extension)

def getUserConfig(conn, user):
    roots = getRoots(conn, user).fetchall()
    extensions = getExtensions(conn, user).fetchall()
    config.WATCHED_EXTENSIONS = []
    config.WATCHED_ROOTS =[]
    for root in roots:
        config.WATCHED_ROOTS.append(root[0])
    for extension in extensions:
        config.WATCHED_EXTENSIONS.append(extension[0])
    config.PERIOD = getPeriod(conn, user).fetchone()[0]
    
def saveNewExtensions(conn, user):
    deleteExtensions(conn, user)
    for extension in config.WATCHED_EXTENSIONS:
        addExtension(conn, user, extension)
    
def saveNewRoots(conn, user):
    deleteRoots(conn, user)
    for root in config.WATCHED_ROOTS:
        addRoot(conn, user, root)

def saveNewPeriod(conn, user):
    modifyPeriod(conn, user, config.PERIOD)