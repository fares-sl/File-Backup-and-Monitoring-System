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
    conn.execute("""
    CREATE TABLE IF NOT EXISTS device (
        device_id INTEGER PRIMARY KEY
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS user (
        user TEXT PRIMARY KEY,
        period INTEGER NOT NULL
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS root (
        root TEXT,
        user TEXT NOT NULL
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS extension (
        extension TEXT NOT NULL,
        user TEXT NOT NULL,
        PRIMARY KEY(extension, user)
    )
    """)
    return conn

def getActions(conn, user):
    return conn.execute("""
    SELECT * FROM actions WHERE user = ? ORDER BY id ASC;
    """,(user,))


def createAction(conn, pathName, action, user, actionTime, oldPath):
    conn.execute("""INSERT INTO actions (filepath, action, user, action_time, old_path)
     VALUES (?,?,?,?,?);""",
     (pathName, action, user, actionTime, oldPath)
     )
    conn.commit()

def fetchLastAction(conn, filePath, user):
    cur = conn.execute('SELECT action FROM actions WHERE user = ? AND filePath = ? AND id = (SELECT MAX(id) FROM actions WHERE user = ? AND filePath = ?);',(user, filePath, user, filePath))
    result = cur.fetchone()
    return result[0] if result else None 

def flushActions(conn, maxActionId, user):
    conn.execute('DELETE FROM actions WHERE user = ? AND id <= ?',(user, maxActionId))
    conn.commit()

def savedeviceId(conn, device_id):
    conn.execute(
        "INSERT INTO device (device_id) VALUES (?)",
        (device_id,)
    )
    conn.commit()


def getdeviceId(conn):
    result = conn.execute(
        "SELECT device_id FROM device"
    ).fetchone()

    return result[0] if result else None


def addNewUser(conn, user ,period):
    conn.execute("INSERT INTO user (user, period) VALUES (?, ?)",(user, period))
    conn.commit()


def addRoot(conn, user, root):
    conn.execute("INSERT INTO root (root, user) VALUES (?, ?)",(root, user))
    conn.commit()


def addExtension(conn, user, extension):
    conn.execute("INSERT INTO extension (extension, user) VALUES (?, ?)",(extension, user))
    conn.commit()

def modifyPeriod(conn, user, period):
    conn.execute('UPDATE user SET period = ? WHERE user = ?',(period, user))
    conn.commit()


def getRoots(conn, user):
    return conn.execute('SELECT root FROM root WHERE user = ?',(user,))


def getExtensions(conn, user):
    return conn.execute('SELECT extension FROM extension WHERE user = ?', (user,))


def getPeriod(conn, user):
    return conn.execute('SELECT period from user WHERE user = ?',(user,))

def findUser(conn, user):
    return conn.execute('SELECT * FROM user WHERE user = ?',(user,)).fetchone() is not None


def deleteExtensions(conn, user):
    conn.execute('DELETE from extension WHERE user = ?',(user,))
    conn.commit()


def deleteRoots(conn, user):
    conn.execute('DELETE FROM root WHERE user = ?',(user,))
    conn.commit()

def initializeActionId(conn, id):
    conn.execute('INSERT INTO actions (id ,filepath, action, user, action_time, old_path) VALUES (?,?,?,?,?,?);',(id,'a','delete','a','a','a'))
    conn.commit()
    conn.execute('DELETE FROM actions;')
    conn.commit()
