from fastapi import FastAPI
import os

from services.fetch_store import start_background_fetch
from services.stocks import router as stocks_router

app = FastAPI()

app.include_router(stocks_router)


@app.get("/")
def home():
    return {"status": "ok"}


# 🔥 VERY IMPORTANT — run only once
@app.on_event("startup")
def startup_event():
    start_background_fetch()
