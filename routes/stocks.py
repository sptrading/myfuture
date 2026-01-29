# routes/stocks.py
from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/stocks")
def get_stocks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT symbol, ltp, change_percent
        FROM stocks
        GROUP BY symbol
        ORDER BY timestamp DESC
        LIMIT 200
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {"symbol": r[0], "ltp": r[1], "change_percent": r[2]}
        for r in rows
    ]
