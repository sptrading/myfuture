# runner.py
import time
from services.fetch_store import fetch_and_store

# तुझ्या instruments list इथे टाक (200+)
instrument_keys = [
    "NSE_EQ|INE466L01038",
    "NSE_EQ|INE117A01022",
    # बाकी तुझे keys
]

while True:
    try:
        fetch_and_store(instrument_keys)
        time.sleep(30)
    except Exception as e:
        print("Runner Error:", e)
        time.sleep(10)
