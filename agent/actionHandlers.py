from local_db import fetchLastAction, createAction
from classes import Action
from utilities import getTime , getUser
from config import WATCHED_EXTENSIONS, WATCHED_ROOTS


def actionHandler(conn, filePath, action, oldPath = None):
    createAction(conn, filePath, action, getUser(), getTime(), oldPath)
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

def moveFileHandler(conn, filePath, oldPath):
    action = Action.MOVE
    actionHandler(conn, filePath, action.value, oldPath)

