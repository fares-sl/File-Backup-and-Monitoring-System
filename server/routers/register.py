from fastapi import APIRouter
from database.db_services import generateDeviceId, getLastDeviceResolvedActionId
from models.DeviceRegister import DeviceRegister

router = APIRouter()

@router.post('/api/register')

def register_Device(registerObject : DeviceRegister) :
    device_id = generateDeviceId(registerObject.hostName, registerObject.platform, registerObject.mac)
    return {"device_id": device_id, 'last_action_id': getLastDeviceResolvedActionId(device_id)}
