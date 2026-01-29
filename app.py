from fastapi import FastAPI
from routes.stocks import router as stocks_router
from services.fetch_store import start_background_fetch

app = FastAPI()

# Include routes
app.include_router(stocks_router)

@app.on_event("startup")
def startup_event():
    start_background_fetch()


@app.get("/")
def home():
    return {"status": "ok"}
