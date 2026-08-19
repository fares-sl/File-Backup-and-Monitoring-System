import sqlite3

def createConnection():
    conn = sqlite3.connect('agent.db', timeout = 5.0)
    conn.execute("""CREATE TALBE IF NOT EXISTS paths (
                filepath STRING PRIMARY KEY,
                action_count INTEGER 
                )"""
    )