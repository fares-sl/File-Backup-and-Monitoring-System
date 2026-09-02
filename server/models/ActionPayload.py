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
    agent_id : int
    hostName : str
    actions : list[Action]

    def getDeviceId(self):
        return self.agent_id


