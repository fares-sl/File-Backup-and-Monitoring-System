import sqlite3

def createConnection(dbName):
    conn = sqlite3.connect(dbName, timeout = 5.0)
    conn.execute("""CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filepath TEXT,
    action TEXT NOT NULL CHECK(action in ("create","delete","modify","move")),
    user TEXT NOT NULL,
    action_time TEXT NOT NULL,
    old_path TEXT NULL
    )
    """
    )
    return conn

def getActions(conn):
    return conn.execute("""
    SELECT * FROM actions ORDER BY id ASC;
    """)


def createAction(conn, pathName, action, user, actionTime, oldPath):
    conn.execute("""INSERT INTO actions (filepath, action, user, action_time, old_path)
     VALUES (?,?,?,?,?);""",
     (pathName, action, user, actionTime, oldPath)
     ) 

def fetchLastAction(conn, filePath):
    cur = conn.execute('SELECT action FROM actions WHERE filePath = ? AND id = (SELECT MAX(id) FROM actions WHERE filePath = ?);',(filePath,filePath))
    result = cur.fetchone()
    return result[0] if result else None 

def flushActions(conn, maxActionId):
    conn.execute('DELETE FROM actions WHERE id <= ?',(maxActionId,))
    conn.commit()


