from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/stocks")
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
