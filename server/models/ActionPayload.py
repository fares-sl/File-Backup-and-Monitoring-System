from pydantic import BaseModel
from enum import Enum

class ActionType(str, Enum):
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
    MOVE = "move"

class Action(BaseModel):
    id : int
    path : str
    action : ActionType
    user : str
    time : str
    oldPath : str | None = None

class ActionPayload(BaseModel):
    device_id : int
    user : str
    actions : list[Action]

    def getDeviceId(self):
        return self.device_id


