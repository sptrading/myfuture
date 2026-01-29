from fastapi import FastAPI
from routes.stocks import router as stocks_router
from services.fetch_store import fetch_and_store
import threading
import time

app = FastAPI()
app.include_router(stocks_router)

instrument_keys = [
    "NSE_EQ|INE466L01038",
    "NSE_EQ|INE117A01022",
    # बाकी तुझे keys
]

def background_runner():
    while True:
        try:
            fetch_and_store(instrument_keys)
            time.sleep(30)
        except Exception as e:
            print("Background Error:", e)
            time.sleep(10)

@app.on_event("startup")
def start_background_task():
    thread = threading.Thread(target=background_runner, daemon=True)
    thread.start()

@app.get("/")
def home():
    return {"message": "Upstox Scanner Running"}
