import sqlite3

DB_NAME = "registrations.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
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


def get_all():

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM registrations ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return rows


def count():

    conn = get_db()

    result = conn.execute(
        "SELECT COUNT(*) FROM registrations"
    ).fetchone()[0]

    conn.close()

    return result


init_db()
