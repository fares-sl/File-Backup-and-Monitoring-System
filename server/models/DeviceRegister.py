from pydantic import BaseModel

class DeviceRegister(BaseModel):
    hostName : str
    platform : str
    mac : list[str]
