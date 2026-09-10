from fastapi import APIRouter
from database.db_services import generateDeviceId
from models.DeviceRegister import DeviceRegister

router = APIRouter()

@router.post('/api/register')

def register_Device(registerObject : DeviceRegister) :
    return {"device_id": generateDeviceId(registerObject.hostName, registerObject.platform, registerObject.mac)}
