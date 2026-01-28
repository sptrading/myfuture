from fastapi import FastAPI
from routes.stocks import router as stocks_router
from services.fetch_store import start_fetch_loop
import threading

app = FastAPI()

app.include_router(stocks_router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    threading.Thread(target=start_fetch_loop, daemon=True).start()
