from enum import Enum

class Action(Enum):
    CREATE = 'create'
    MODIFY = 'modify'
    DELETE = 'delete'
    MOVE = 'move'

class ActionObject:
    def __init__(self, id, path, action, user, actionTime, oldPath):
        self.id = id
        self.path = path
        self.action = action
        self.user = user
        self.actionTime = actionTime
        self.oldPath = oldPath
    
    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "action": self.action,
            "user": self.user,
            "time": self.actionTime,
            "oldPath": self.oldPath
        }


class Payload:
    def __init__(self, hostName, agent_id, actions):
        self.hostName = hostName
        self.agent_id = agent_id
        self.actions = actions

    def noAction(self):
        return not self.actions

    def getMaxActionId(self):
        return self.actions[-1].id

    def to_dict(self):
        return {
            "hostName": self.hostName,
            "agent_id": self.agent_id,
            "actions": [
                action.to_dict()
                for action in self.actions
            ]
        }

    
    
def getActionsList(actionsTuplesList):
    actionsList = []
    for action in actionsTuplesList:
        actionsList.append(ActionObject(action[0], action[1], action[2], action[3], action[4], action[5]))
    return actionsList



