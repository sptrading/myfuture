import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "stocks.db")

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            symbol TEXT,
            ltp REAL,
            prev_close REAL,
            change_percent REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
