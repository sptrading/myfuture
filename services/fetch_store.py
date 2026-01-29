# services/fetch_store.py
import requests
import os
from services.database import get_connection

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

URL = "https://api.upstox.com/v2/market-quote/quotes"

def fetch_and_store(instrument_keys):
    conn = get_connection()
    cursor = conn.cursor()

    params = {
        "instrument_key": ",".join(instrument_keys)
    }

    response = requests.get(URL, headers=HEADERS, params=params)
    data = response.json()

    for key, value in data.get("data", {}).items():
        ltp = value.get("last_price", 0)
        prev = value.get("prev_close", 0)

        if prev == 0:
            continue

        change_percent = ((ltp - prev) / prev) * 100

        cursor.execute("""
            INSERT INTO stocks (symbol, ltp, prev_close, change_percent)
            VALUES (?, ?, ?, ?)
        """, (key, ltp, prev, change_percent))

    conn.commit()
    conn.close()
