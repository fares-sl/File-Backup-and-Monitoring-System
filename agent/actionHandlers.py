from local_db import fetchLastAction, createAction
from classes import Action
from utilities import getTime , getUser
import config


def actionHandler(conn, filePath, action, oldPath = None):
    createAction(conn, filePath, action, getUser(), getTime(), oldPath)


def createFileHandler(conn, filePath):
    action = Action.CREATE
    actionHandler(conn, filePath, action.value)


def modifyFileHandler(conn, filePath):
    action = Action.MODIFY
    if fetchLastAction(conn, filePath, config.USER) != action.value:
        actionHandler(conn, filePath, action.value)

def deleteFileHandler(conn, filePath):
    action = Action.DELETE
    actionHandler(conn, filePath, action.value)

def moveFileHandler(conn, filePath, oldPath):
    action = Action.MOVE
    actionHandler(conn, filePath, action.value, oldPath)

