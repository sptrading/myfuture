from fastapi import APIRouter
from services.database import get_connection

router = APIRouter()


@router.get("/stocks")
def get_stocks():
    conn = get_connection()
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
