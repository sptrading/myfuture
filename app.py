from fastapi import FastAPI
import threading
import sqlite3

from services.fetch_store import start_fetch_loop
from services.database import init_db

app = FastAPI()

# DB init
init_db()


@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_fetch_loop, daemon=True)
    thread.start()
    print("🚀 Background fetch started")


# 👇 Render health check साठी IMPORTANT
@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/stocks")
def get_stocks():
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()

    c.execute("""
        SELECT symbol, ltp, change_percent
        FROM stock_data
        ORDER BY timestamp DESC
        LIMIT 200
    """)

    rows = c.fetchall()
    conn.close()

    return rows
from fetch_store import start_background_fetch

@app.on_event("startup")
def startup_event():
    start_background_fetch()
