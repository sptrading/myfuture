# app.py
from fastapi import FastAPI
from routes.stocks import router as stocks_router

app = FastAPI()

app.include_router(stocks_router)

@app.get("/")
def home():
    return {"message": "Upstox Scanner Running"}
