import requests
import sqlite3
import threading
import time
import os

from services.instrument_map import INSTRUMENT_MAP

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

_started = False


def fetch_and_store():
    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    keys = list(INSTRUMENT_MAP.values())

    while True:
        try:
            conn = sqlite3.connect("stocks.db")
            c = conn.cursor()

            # Table create
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
                batch = keys[i:i + batch_size]

                params = {
                    "instrument_key": ",".join(batch)
                }

                print(f"📥 Fetching batch {i} to {i+batch_size}")

                res = requests.get(url, headers=headers, params=params, timeout=15)
                data = res.json().get("data", {})

                for symbol, key in INSTRUMENT_MAP.items():
                    if key in batch:
                        quote = data.get(key, {})

                        ltp = quote.get("last_price", 0)

                        # prev_close मिळत नाही ltp endpoint मधून
                        prev = 0
                        change = 0

                        c.execute("""
                            INSERT INTO stock_data (symbol, ltp, prev_close, change_percent)
                            VALUES (?, ?, ?, ?)
                        """, (symbol, ltp, prev, change))

            conn.commit()
            conn.close()

            print("✅ Updated. Sleeping 60s\n")
            time.sleep(60)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(10)


def start_background_fetch():
    global _started

    if _started:
        return

    _started = True

    thread = threading.Thread(target=fetch_and_store, daemon=True)
    thread.start()
    print("🚀 Background fetch started")
