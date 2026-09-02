from fastapi import APIRouter
from models.ActionPayload import ActionPayload
from models.AgentConfig import AgentConfig
from services.action_services import filterResolvedActions, SaveNewLogs, getequivalentActionsList, resolveActions
from db_services import fetchExtensions, fetchPeriod, fetchRoots

router = APIRouter()

@router.post("/api/actions")
def receive_actions(payload : ActionPayload) -> AgentConfig :
    actions = filterResolvedActions(payload)
    SaveNewLogs(actions)
    device_folder = str(payload.agent_id)
    equivalentActionsList = getequivalentActionsList(actions, device_folder)
    filesToUpload = resolveActions(equivalentActionsList, device_folder)
    deviceId = payload.agent_id
    return AgentConfig(fetchRoots(deviceId), fetchExtensions(deviceId), fetchPeriod(deviceId), filesToUpload)
