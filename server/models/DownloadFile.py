from pydantic import BaseModel

class DownloadFile(BaseModel):
    device_id : int
    user : str
    path : str