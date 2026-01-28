import requests
import sqlite3
import os
import time

from services.instrument_map import INSTRUMENT_MAP

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

URL = "https://api.upstox.com/v2/market-quote/quotes"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}


def start_fetch_loop():
    print("🚀 Background fetch started")

    symbols = list(INSTRUMENT_MAP.items())

    while True:
        try:
            conn = from services.database import get_connection
            c = conn.cursor()

            for i in range(0, len(symbols), 40):
                batch = symbols[i:i+40]
                keys = ",".join([key for _, key in batch])

                params = {"instrument_keys": keys}
                res = requests.get(URL, headers=HEADERS, params=params)
                data = res.json().get("data", {})

                for symbol, key in batch:
                    if key in data:
                        quote = data[key]
                        ltp = quote.get("ltp", 0)
                        prev = quote.get("cp", 0)
                        change = ((ltp - prev) / prev) * 100 if prev else 0

                        c.execute("""
                            INSERT INTO stock_data (symbol, ltp, prev_close, change_percent)
                            VALUES (?, ?, ?, ?)
                        """, (symbol, ltp, prev, change))

            conn.commit()
            conn.close()

            print("✅ Updated. Sleeping 60s")
            time.sleep(60)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)
import threading

_started = False

def start_background_fetch():
    global _started

    if _started:
        return

    _started = True

    thread = threading.Thread(target=run_fetch_loop, daemon=True)
    thread.start()
    print("🚀 Background fetch started")
