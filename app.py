from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routes.stocks import router as stocks_router

app = FastAPI()

# Templates setup
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(stocks_router)


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
