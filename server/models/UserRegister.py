from pydantic import BaseModel

class UserRegister(BaseModel):
    device_id : int
    user : str
    watched_roots : list[str]
    watched_extensions : list[str]
    period : int

