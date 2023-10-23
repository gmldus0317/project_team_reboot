from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse, FileResponse

from pydantic import BaseModel

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="statics"), name="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request":request})

@app.get("/menu")
async def menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request":request})