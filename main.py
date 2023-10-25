from fastapi import FastAPI, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database import engineconn
from models import Menu

from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="statics"), name="static")
engine = engineconn()

def get_db():
    session = engine.session_maker()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request":request})

@app.get("/menu")
async def menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request":request})

@app.get("/info/{menu_id}")
async def info(request: Request, menu_id: int, db: Session = Depends(get_db)):
    crn_info = db.query(Menu).filter(Menu.menu_id == menu_id).first() # current_information
    dt_info = db.query(Menu).order_by(Menu.menu_id.desc())
    return templates.TemplateResponse("notice.html", {"request": request, "dt_info": dt_info, "crn_info": crn_info})

@app.get("/db")
async def first_get(request: Request, db: Session = Depends(get_db)):
    dt_info = db.query(Menu).order_by(Menu.menu_id.desc())
    if dt_info.count() == 0:
        dt_info = 0

    return templates.TemplateResponse("db_test.html", {"request":request, "dt_info":dt_info})