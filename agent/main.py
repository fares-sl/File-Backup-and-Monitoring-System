from watcher import ChangeHandler, ConfigurateWatchers 
from watchdog.observers import Observer
from utilities import getPayload, sendPayload, uploadFiles, registerWithServer, getUser, registerUser, addUser, getUserConfig, getDefaultWatchedRoot, saveNewRoots, saveNewExtensions, saveNewPeriod
import config
from local_db import createConnection, flushActions, getdeviceId, savedeviceId, findUser, initializeActionId
import time


conn = createConnection(config.AGENT_DB)
device_id = getdeviceId(conn)
if device_id is None:
    device_config = registerWithServer()
    if device_config is None:
        print("Could not register agent with server.")
        conn.close()
        raise SystemExit(1)
    device_id = device_config['device_id']
    initializeActionId(conn, device_config['last_action_id'])
    savedeviceId(conn, device_id)
print(f'agent id: {device_id}')
user = getUser()
config.USER = user
if not findUser(conn, user):
    config.WATCHED_ROOTS = [getDefaultWatchedRoot()]
    if registerUser(user, device_id) is None:
        print('could not register user with the server')
        raise SystemExit(2)
    addUser(conn, user, config.WATCHED_ROOTS, config.WATCHED_EXTENSIONS, config.PERIOD)
getUserConfig(conn, user)
handler = ChangeHandler()
observer = Observer()
watchers = {}
ConfigurateWatchers(observer, handler, watchers, config.WATCHED_ROOTS)
observer.start()
while True:
    time.sleep(config.PERIOD)
    payload = getPayload(conn, device_id, user)
    respond = sendPayload(payload)
    if respond is not None:
        if config.WATCHED_ROOTS != respond['roots']:
            config.WATCHED_ROOTS = respond['roots']
            ConfigurateWatchers(observer, handler, watchers, config.WATCHED_ROOTS)
            saveNewRoots(conn, user)
        if config.WATCHED_EXTENSIONS != respond['extensions']:
            config.WATCHED_EXTENSIONS = respond['extensions']
            saveNewExtensions(conn, user)
        if config.PERIOD != respond['period']:
            config.PERIOD = respond['period']
            saveNewPeriod(conn, user)
        if not payload.noAction():
            maxActionId = payload.getMaxActionId()
            print(maxActionId)
            flushActions(conn, maxActionId, user)
            uploadFiles(respond['paths'], device_id)