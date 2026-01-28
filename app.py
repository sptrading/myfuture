from fastapi import FastAPI
from stocks import router as stocks_router
from fetch_store import start_background_fetch

app = FastAPI()

app.include_router(stocks_router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    start_background_fetch()
