from models.ActionPayload import ActionPayload
from database.db_services import getLastResolvedActionId, saveAction
from pathlib import Path
import config
import shutil

def filterResolvedActions(payload):
        lastResolvedAction = getLastResolvedActionId(payload.agent_id, payload.user)
        while payload.actions and payload.actions[0].id <= lastResolvedAction :
            payload.actions.pop(0)
        return payload.actions

def SaveNewLogs(actions, agent_id):
        for action in actions :
            saveAction(action, agent_id)

def concatenatePaths(backup_root, device_folder, agent_path):
    relative_path = agent_path.lstrip("/")
    relative_path = relative_path.replace("\\", "/")
    return str(
        Path(backup_root) / device_folder / relative_path
    )
    
def equivalentAction(actionA):
    if actionA == 'create':
        return 'create'
    return 'modify'

def createFile(path):
    path = Path(path)
    if path.exists():
        print(f'file f{path} already exists')
        return False
    try:
        path.parent.mkdir(parents = True, exist_ok = True)
        path.touch()
        print(f'file {path} created')
        return True
    except OSError as e:
        print(f"Could not create {path}: {e}")
        return False

def moveFile(oldPath, newPath):
    oldPath = Path(oldPath)
    if not oldPath.exists():
        print(f'file f{oldPath} does not exists')
        return False
    newPath = Path(newPath)
    if newPath.exists():
        print(f'file f{newPath} already exists')
        return False
    try:
        newPath.parent.mkdir(parents = True, exist_ok = True)
        shutil.move(str(oldPath), str(newPath))
        print(f"File {oldPath} moved to {newPath}")
        return True
    except OSError as e:
        print(f"Could not move {oldPath} to {newPath}: {e}")
        return False


def deleteFile(path, device_folder, time):
    newPath = concatenatePaths(config.BIN_ROOT, device_folder, path + '_' + time.replace(':', '-').replace(' ', '_'))
    oldPath = concatenatePaths(config.BACKUP_ROOT, device_folder, path)
    moveFile(oldPath, newPath)


def getequivalentActionsList(actions, device_folder):
    actionDict = {}
    for action in actions :
        if action.action.value == 'move':
            moveFile(concatenatePaths(config.BACKUP_ROOT, device_folder,action.oldPath), concatenatePaths(config.BACKUP_ROOT, device_folder,action.path))
            if action.oldPath in actionDict:
                actionDict[action.path] = 'create'
                del actionDict[action.oldPath]
        elif action.action.value == 'delete':
            deleteFile(action.path, device_folder, action.time)
            if action.path in actionDict:
                del actionDict[action.path]
        else:
            if action.path in actionDict:
                actionDict[action.path] = equivalentAction(actionDict[action.path])
            else:
                actionDict[action.path] = action.action.value
    return actionDict

def resolveActions(actionDict, device_folder):
    filesToUpload = []
    for path in actionDict:
        fullPath = concatenatePaths(config.BACKUP_ROOT, device_folder, path)
        createFile(fullPath)
        filesToUpload.append(path)
    return filesToUpload