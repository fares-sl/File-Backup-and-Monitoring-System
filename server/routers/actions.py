from fastapi import APIRouter
from models.ActionPayload import ActionPayload
from models.UserConfig import UserConfig
from services.action_services import filterResolvedActions, SaveNewLogs, getequivalentActionsList, resolveActions
from database.db_services import fetchExtensions, fetchPeriod, fetchRoots, fetchPathsToDownload
from services.exceptions_handlers import verifyCredentialsExistence

router = APIRouter()

@router.post("/api/actions")
def receive_actions(payload : ActionPayload) -> UserConfig :
    verifyCredentialsExistence(payload.device_id, payload.user)
    actions = filterResolvedActions(payload)
    print(f"actions to resolve: {actions}")
    SaveNewLogs(actions, payload.device_id)
    device_folder = str(payload.device_id)
    equivalentActionsList = getequivalentActionsList(actions, device_folder)
    print(f'equivalentActions: {equivalentActionsList}')
    filesToUpload = resolveActions(equivalentActionsList, device_folder)
    print('files to upload: ', filesToUpload)
    deviceId = payload.device_id
    return UserConfig(
    roots=fetchRoots(deviceId, payload.user),
    extensions=fetchExtensions(deviceId, payload.user),
    period=fetchPeriod(deviceId, payload.user),
    paths=filesToUpload,
    paths_to_download = fetchPathsToDownload(deviceId, payload.user)
    )