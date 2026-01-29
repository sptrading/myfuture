import requests
import sqlite3
import threading
import time
import os

from services.instrument_map import INSTRUMENT_MAP

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

def fetch_and_store():
    url = "https://api.upstox.com/v2/market-quote/quotes"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    keys = list(INSTRUMENT_MAP.values())

    while True:
        try:
            conn = sqlite3.connect("stocks.db")
            c = conn.cursor()

            c.execute("""
                CREATE TABLE IF NOT EXISTS stock_data (
                    symbol TEXT,
                    ltp REAL,
                    prev_close REAL,
                    change_percent REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            c.execute("DELETE FROM stock_data")

            batch_size = 50
            for i in range(0, len(keys), batch_size):
                batch = keys[i:i+batch_size]
                params = {"instrument_key": ",".join(batch)}

                res = requests.get(url, headers=headers, params=params)
                data = res.json().get("data", {})

                for symbol, key in INSTRUMENT_MAP.items():
                    if key in data:
                        quote = data[key]

                        # ✅ CORRECT KEYS FROM UPSTOX
                        ltp = quote.get("ltp")
                        prev = quote.get("close")

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
            print("❌ Error:", e)
            time.sleep(10)


def start_background_fetch():
    thread = threading.Thread(target=fetch_and_store, daemon=True)
    thread.start()
    print("🚀 Background fetch started")
