import os
import time
import threading

from upstox_client import Configuration, ApiClient, MarketQuoteApi
from services.instrument_map import INSTRUMENT_MAP
from services.database import init_db, get_connection

print("✅ FETCH_STORE FILE LOADED")

init_db()

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

configuration = Configuration()
configuration.access_token = ACCESS_TOKEN

api_client = ApiClient(configuration)
quote_api = MarketQuoteApi(api_client)


def fetch_quotes():
    print("🚀 Fetch thread started")

    keys = list(INSTRUMENT_MAP.values())

    while True:
        try:
            conn = get_connection()
            c = conn.cursor()

            print("📥 Fetching quotes from Upstox SDK")

            response = quote_api.get_market_quote(keys)

            data = response.data

            for symbol, key in INSTRUMENT_MAP.items():
                if key in data:
                    quote = data[key]

                    ltp = quote.ltp
                    prev = quote.close_price
                    change = ((ltp - prev) / prev) * 100 if prev else 0

                    c.execute("""
                        INSERT INTO stock_data (symbol, ltp, prev_close, change_percent)
                        VALUES (?, ?, ?, ?)
                    """, (symbol, ltp, prev, change))

            conn.commit()
            conn.close()

            print("✅ Data inserted. Sleeping 60s\n")
            time.sleep(60)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(10)


threading.Thread(target=fetch_quotes, daemon=True).start()
