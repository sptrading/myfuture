import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "stocks.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT,
            ltp REAL,
            prev_close REAL,
            change_percent REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn
