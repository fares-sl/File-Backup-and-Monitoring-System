import local_db
from classes import action
from utilities import getTime , getUser

def createFileHandler(conn, filePath):
    action = Action.CREATE
    actionCount = searchPath(conn, filePath)
    if not actionCount:
        createPath(conn, filePath)
    createAction(conn, filePath, action.value, actionCount + 1, getUser(), getTime())
    modifyActionCount(conn, filePath, actionCount + 1)

def modifyFileHandler(conn, filePath):
    