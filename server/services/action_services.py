from models.ActionPayload import ActionPayload
from db_services import getLastResolvedActionId, saveAction
from pathlib import Path
from config import BACKUP_ROOT


def filterResolvedActions(payload):
        lastResolvedAction = getLastResolvedActionId(payload.agent_id)
        while payload.actions and payload.actions[0].id <= lastResolvedAction :
            payload.actions.pop(0)
        return payload.actions

def SaveNewLogs(actions):
        for action in actions :
            saveAction(action)

def concatenatePaths(backup_root, device_folder, agent_path):
    relative_path = agent_path.lstrip("/")
    relative_path = relative_path.replace("\\", "/")
    return str(
        Path(backup_root) / device_folder / relative_path
    )
    
def equivalentAction(actionA, actionB):
    if actionA == 'create':
        return 'create'
    return 'modify'

def createFile(path):
    print(f'file {path} created')

def deleteFile(path):
    print(f'file {path} deleted')

def moveFile(oldPath, newpath):
    print(f'{oldPath} moved to {newpath}')


def getequivalentActionsList(actions, device_folder):
    actionDict = {}
    for action in actions :
        if action.action.value == 'move':
            moveFile(concatenatePaths(BACKUP_ROOT, device_folder,action.oldPath), concatenatePaths(BACKUP_ROOT, device_folder,action.path))
            if action.oldPath in actionDict:
                actionDict[action.path] = 'create'
                del actionDict[action.oldPath]
        elif action.action.value == 'delete':
            deleteFile(concatenatePaths(BACKUP_ROOT, device_folder,action.path))
            if action.path in actionDict:
                del actionDict[action.path]
        else:
            if action.path in actionDict:
                actionDict[action.path] = equivalentAction(actionDict[action.path], action.action.value)
            else:
                actionDict[action.path] = action.action.value
    return actionDict

def resolveActions(actionDict, device_folder):
    filesToUpload = []
    for path in actionDict:
        fullPath = concatenatePaths(BACKUP_ROOT, device_folder, path)
        match (actionDict[path]):
            case 'create':
                createFile(fullPath)
                filesToUpload.append(path)
            case 'modify':
                filesToUpload.append(path)
            case 'delete':
                deleteFile(fullPath)
    return filesToUpload