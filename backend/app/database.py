import sqlite3
from pathlib import Path
from .config import DATABASE_URL

DB_FILE = Path(__file__).resolve().parent.parent / 'data.db'


def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS hcp_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hcp_name TEXT NOT NULL,
            interaction_type TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            attendees TEXT,
            topics TEXT,
            sentiment TEXT,
            outcomes TEXT,
            follow_up TEXT,
            notes TEXT,
            ai_summary TEXT
        )
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY(interaction_id) REFERENCES hcp_interactions(id) ON DELETE CASCADE
        )
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            quantity TEXT,
            FOREIGN KEY(interaction_id) REFERENCES hcp_interactions(id) ON DELETE CASCADE
        )
        '''
    )
    conn.commit()
    conn.close()
