from enum import Enum

class Action(Enum):
    CREATE = 'create'
    MODIFY = 'modify'
    DELETE = 'delete'
    MOVE = 'move'

class Payload:
    def __init__(self, hostName, actions):
        self.hostName = hostName
        self.actions = actions

    def noAction(self):
        return not self.actions

    def getMaxActionId(self):
        return self.actions[-1][0]
    

