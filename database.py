import sqlite3

def init_db():
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    cursor.execute ("""
    CREATE TABLE IF NOT EXISTS vault(
        id INTEGER PRIMARY KEY AUTOINCREMENT    ,
        website     TEXT NOT NULL,
        username    TEXT NOT NULL,
        password    TEXT NOT NULL
    )
""")
    
    conn.commit()
    return conn