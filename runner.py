# runner.py
import time
from fetch_store import fetch_and_store

# तुझ्या instruments.json मधून घे
instrument_keys = [
    "NSE_EQ|INE466L01038",
    "NSE_EQ|INE117A01022",
    # बाकी तुझे 200+ keys इथे
]

while True:
    fetch_and_store(instrument_keys)
    time.sleep(30)
