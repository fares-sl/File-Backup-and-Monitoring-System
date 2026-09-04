from fastapi import APIRouter
from models.ActionPayload import ActionPayload
from models.AgentConfig import AgentConfig
from services.action_services import filterResolvedActions, SaveNewLogs, getequivalentActionsList, resolveActions
from database.db_services import fetchExtensions, fetchPeriod, fetchRoots

router = APIRouter()

@router.post("/api/actions")
def receive_actions(payload : ActionPayload) -> AgentConfig :
    actions = filterResolvedActions(payload)
    print(f"actions to resolve: {actions}")
    SaveNewLogs(actions, payload.agent_id)
    device_folder = str(payload.agent_id)
    equivalentActionsList = getequivalentActionsList(actions, device_folder)
    print(f'equivalentActions: {equivalentActionsList}')
    filesToUpload = resolveActions(equivalentActionsList, device_folder)
    print('files to upload: ', filesToUpload)
    deviceId = payload.agent_id
    return AgentConfig(
    roots=fetchRoots(deviceId),
    extensions=fetchExtensions(deviceId),
    period=fetchPeriod(deviceId),
    paths=filesToUpload
    )