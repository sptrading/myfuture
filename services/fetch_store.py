import requests
import sqlite3
import os
import time
import threading

from services.instrument_map import INSTRUMENT_MAP
from services.database import init_db, get_connection

print("✅ FETCH_STORE FILE LOADED")

init_db()

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

URL = "https://api.upstox.com/v2/market-quote/quotes"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}


def fetch_quotes():
    print("🚀 Fetch thread started")

    keys = list(INSTRUMENT_MAP.values())

    while True:
        try:
            conn = get_connection()
            c = conn.cursor()

            # 40-40 च्या batch मध्ये
            for i in range(0, len(keys), 40):
                batch = keys[i:i+40]
                print(f"📥 Fetching batch {i} to {i+40}")

                res = requests.post(
                    URL,
                    headers=HEADERS,
                    json={"instrument_key": batch}   # ⚠️ singular
                )

                data = res.json().get("data", {})

                for symbol, key in INSTRUMENT_MAP.items():
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

            print("✅ All batches inserted. Sleeping 60s\n")
            time.sleep(60)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(10)


threading.Thread(target=fetch_quotes, daemon=True).start()
