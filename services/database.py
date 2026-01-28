import sqlite3

def init_db():
    conn = sqlite3.connect("stocks.db")
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
