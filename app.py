from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routes.stocks import router as stocks_router
from services.fetch_store import start_background_fetch

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(stocks_router)


# Start background Upstox fetch when app starts



# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
