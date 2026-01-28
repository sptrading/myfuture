import requests
import sqlite3
import os
import time

from services.instrument_map import INSTRUMENT_MAP
from services.database import init_db

init_db()

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

URL = "https://api.upstox.com/v2/market-quote/quotes"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}


def fetch_and_store():
    print("🚀 Fetch thread started")

    symbols = list(INSTRUMENT_MAP.items())

    while True:
        try:
            conn = sqlite3.connect("stocks.db")
            c = conn.cursor()

            # 40 keys per batch (Upstox limit safe)
            for i in range(0, len(symbols), 40):
                batch = symbols[i:i+40]
                keys = ",".join([key for _, key in batch])

                print(f"📥 Fetching batch {i} to {i+40}")

                params = {
                    "instrument_keys": keys
                }

                res = requests.get(URL, headers=HEADERS, params=params)
                data = res.json().get("data", {})

                for symbol, key in batch:
                    if key in data:
                        quote = data[key]

                        # ✅ Correct fields from Upstox
                        ltp = quote.get("ltp", 0)
                        prev = quote.get("cp", 0)

                        change = ((ltp - prev) / prev) * 100 if prev else 0

                        c.execute("""
                            INSERT INTO stock_data (symbol, ltp, prev_close, change_percent)
                            VALUES (?, ?, ?, ?)
                        """, (symbol, ltp, prev, change))

            conn.commit()
            conn.close()

            print("✅ All batches inserted. Sleeping 60s\n")
            time.sleep(60)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(10)


# 👇 Auto start when file loads
fetch_and_store()
