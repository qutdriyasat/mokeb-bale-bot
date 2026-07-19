import sqlite3

DB_NAME = "registrations.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():

    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS registrations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE,
        full_name TEXT,
        mobile TEXT,
        national_id TEXT,
        passport TEXT,
        gender TEXT,
        arrival_date TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


init_db()
