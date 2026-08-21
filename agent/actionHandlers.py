import local_db
from classes import action
from utilities import getTime , getUser

def actionHandler(conn, filePath, action):
    actionCount = fetchActionCount(conn, filePath)
    createAction(conn, filePath, action.value, actionCount + 1, getUser(), getTime())
    modifyActionCount(conn, filePath, actionCount + 1)
    conn.commit()


def createFileHandler(conn, filePath):
    action = Action.CREATE
    actionHandler(conn, filePath, action.value)


def modifyFileHandler(conn, filePath):
    action = Action.MODIFY
    if fetchLastAction(conn, filePath) != action.value:
        actionHandler(conn, filePath, action.value)

def deleteFileHandler(conn, filePath):
    action = Action.DELETE
    actionHandler(conn, filePath, action.value)

def moveFileHandler(conn, filePath):
    action = Action.MOVE
    actionHandler(conn, filePath, action.value)
    
