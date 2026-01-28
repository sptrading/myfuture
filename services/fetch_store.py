import requests
import sqlite3
import os
import time

from services.instrument_map import INSTRUMENT_MAP
from services.database import init_db

init_db()

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

def fetch_quotes():
    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    keys = ",".join(INSTRUMENT_MAP.values())

    params = {
        "instrument_key": keys
    }

    res = requests.get(url, headers=headers, params=params)
    data = res.json()["data"]

    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()

    for symbol, key in INSTRUMENT_MAP.items():
        quote = data.get(key, {})
        ltp = quote.get("last_price", 0)
        prev = quote.get("prev_close", 0)

        change = ((ltp - prev) / prev) * 100 if prev else 0

        c.execute('''
            INSERT INTO stock_data (symbol, ltp, prev_close, change_percent)
            VALUES (?, ?, ?, ?)
        ''', (symbol, ltp, prev, change))

    conn.commit()
    conn.close()

while True:
    fetch_quotes()
    time.sleep(60)
