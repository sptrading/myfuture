from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import services.fetch_store  # 👈 THIS IS THE KEY

from routes.stocks import router as stocks_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(stocks_router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
