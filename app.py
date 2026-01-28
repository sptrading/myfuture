from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import services.fetch_store  # 👈 MUST

from routes.stocks import router as stocks_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(stocks_router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
from fastapi import FastAPI
import threading

from services.fetch_store import start_fetch_loop

app = FastAPI()

@app.on_event("startup")
def start_background_thread():
    thread = threading.Thread(target=start_fetch_loop, daemon=True)
    thread.start()
