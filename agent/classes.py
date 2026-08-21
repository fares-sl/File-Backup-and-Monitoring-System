from enum import Enum

class Action(Enum):
    CREATE = 'create'
    MODIFY = 'modify'
    DELETE = 'delete'
    MOVE = 'move'

class Payload:
    def __init__(self, hostName, pathActions):
        self.hostName = hostName
        self.pathActions = pathActions

    def generateMaxActionPairList(self):
        maxActionList = []
        for pathAction in self.pathActions:
            maxActionList.append(
                (pathAction.pathName, pathAction.maxActionNumber)
            )
        return maxActionList
    
    def to_dict(self):
        return {
            "hostName": self.hostName,
            "pathActions": [
                path.to_dict()
                for path in self.pathActions
            ]
        }

class PathActions:
    def __init__(self, pathName, maxActionNumber):
        self.pathName = pathName
        self.maxActionNumber = maxActionNumber
        self.actionList = []

    def appendAction(self, action, user, actionTime, oldPath):
        self.actionList.append((action, user, actionTime, oldPath))
        self.maxActionNumber += 1

    def to_dict(self):
        return {
            "pathName": self.pathName,
            "maxActionNumber": self.maxActionNumber,
            "actionList": self.actionList
        }
    
