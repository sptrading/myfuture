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
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    all_keys = list(INSTRUMENT_MAP.values())
    batch_size = 40  # Upstox safe limit

    while True:
        try:
            conn = get_connection()
            c = conn.cursor()

            for i in range(0, len(all_keys), batch_size):
                batch = all_keys[i:i + batch_size]

                print(f"📥 Fetching batch {i} to {i+batch_size}")

                res = requests.post(
                    url,
                    headers=headers,
                    json={"instrument_keys": batch}
                )

                data = res.json().get("data", {})

                for symbol, key in INSTRUMENT_MAP.items():
                    if key in data:
                        quote = data[key]

                        ltp = quote.get("last_price", 0)
                        prev = quote.get("ohlc", {}).get("close", 0)
                        change = ((ltp - prev) / prev) * 100 if prev else 0

                        c.execute("""
                            INSERT INTO stock_data (symbol, ltp, prev_close, change_percent)
                            VALUES (?, ?, ?, ?)
                        """, (symbol, ltp, prev, change))

                time.sleep(1)  # 🔥 batch gap (important)

            conn.commit()
            conn.close()

            print("✅ One full cycle done. Sleeping 60s...\n")
            time.sleep(60)  # 🔥 cycle gap (important)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(10)


# 👇 file load झाला की thread सुरू
threading.Thread(target=fetch_quotes, daemon=True).start()
