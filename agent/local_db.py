import sqlite3

def createConnection():
    conn = sqlite3.connect('agent.db', timeout = 5.0)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""CREATE TABLE IF NOT EXISTS paths (
                filepath TEXT PRIMARY KEY,
                action_count INTEGER 
                )"""
    )
    conn.execute("""CREATE TABLE IF NOT EXISTS actions (
    filepath TEXT REFERENCES paths(filepath),
    action TEXT NOT NULL CHECK(action in ("create","delete","modify","move")),
    action_number INTEGER,
    user TEXT NOT NULL,
    action_time TEXT NOT NULL,
    old_path TEXT NULL,
    PRIMARY KEY(filepath, action_number)
    )
    """
    )
    return conn

def getActions(conn):
    return conn.execute("""
    SELECT * FROM actions ORDER BY filepath ASC, action_number ASC;
    """)

def createPath(conn, pathName):
    conn.execute("INSERT INTO paths (filepath, action_count) VALUES (?, ?);",(pathName, 0))

def searchPath(conn, pathName):
    cur = conn.execute('SELECT action_count FROM paths WHERE filepath = ?;',(pathName,))
    result = cur.fetchone()
    if result is None:
        return 0
    return result[0]

def modifyActionCount(conn, pathName, actionCount):
    conn.execute('UPDATE paths SET action_count = ? WHERE filepath = ?;', (actionCount, pathName))

def createAction(conn, pathName, action, actionNumber, user, actionTime, oldPath=None):
    conn.execute("""INSERT INTO actions (filepath, action, action_number, user, action_time, old_path)
     VALUES (?,?,?,?,?,?);""",
     (pathName, action, actionNumber, user, actionTime, oldPath)
     ) 

def fetchLastAction(conn, filePath):
    cur = conn.execute('SELECT action FROM actions WHERE filePath = ? AND action_number = (SELECT MAX(action_number) FROM actions WHERE filePath = ?);',(filePath,filePath))
    result = cur.fetchone()
    return result[0] if result else None 