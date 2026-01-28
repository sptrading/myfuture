import requests
import sqlite3
import os
import time
import threading

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

    params = {"instrument_key": keys}

    while True:
        try:
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

            time.sleep(60)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)


def start_background_fetch():
    thread = threading.Thread(target=fetch_quotes, daemon=True)
    thread.start()
def start_background_fetch():
    thread = threading.Thread(target=fetch_quotes, daemon=True)
    thread.start()


# 👇 हे IMPORTANT — file load झाला की thread सुरू
start_background_fetch()
