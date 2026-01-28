import requests
import os
import time
import threading

from services.instrument_map import INSTRUMENT_MAP
from services.database import init_db, get_connection

print("✅ FETCH_STORE FILE LOADED")

init_db()

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")


def fetch_quotes():
    print("🚀 Fetch thread started")

    url = "https://api.upstox.com/v2/market-quote/quotes"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    keys = ",".join(INSTRUMENT_MAP.values())
    params = {"instrument_key": keys}

    while True:
        try:
            print("📥 Fetching quotes from Upstox...")

            res = requests.get(url, headers=headers, params=params)
            data = res.json().get("data", {})

            conn = get_connection()
            c = conn.cursor()

            for symbol, key in INSTRUMENT_MAP.items():
                quote = data.get(key, {})
                ltp = quote.get("last_price", 0)
                prev = quote.get("prev_close", 0)
                change = ((ltp - prev) / prev) * 100 if prev else 0

                c.execute("""
                    INSERT INTO stock_data (symbol, ltp, prev_close, change_percent)
                    VALUES (?, ?, ?, ?)
                """, (symbol, ltp, prev, change))

            conn.commit()
            conn.close()

            print("✅ Data inserted into DB")
            time.sleep(60)

        except Exception as e:
            print("❌ Error in fetch:", e)
            time.sleep(10)


# 👇 file load झाला की thread सुरू
threading.Thread(target=fetch_quotes, daemon=True).start()
