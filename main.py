import cryptography # 이 라이브러리가 없으면 오류 발생

from fastapi import FastAPI, Depends, Form, status
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import *
from models import *

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
async def menu(request: Request, db: Session = Depends(get_db)):
    dt_info = db.query(Menu).order_by(Menu.menu_id.desc())
    return templates.TemplateResponse("menu.html", {"request":request, "dt_info": dt_info})

@app.get("/info/{menu_id}")
async def info(request: Request, menu_id: int, db: Session = Depends(get_db)):
    crn_info = db.query(Menu).filter(Menu.menu_id == menu_id).first() # current_information
    dt_info = db.query(Menu).order_by(Menu.menu_id.desc())
    return templates.TemplateResponse("notice.html", {"request": request, "dt_info": dt_info, "crn_info": crn_info})

@app.get("/admin")
async def load_db(request: Request, db: Session = Depends(get_db)):
    dt_info = db.query(Menu).order_by(Menu.menu_id.desc())
    if dt_info.count() == 0:
        dt_info = 0

    return templates.TemplateResponse("db_test.html", {"request":request, "dt_info":dt_info})

@app.get("/edit/{menu_id}")
async def edit_menu(request: Request, menu_id: int, db: Session = Depends(get_db)):
    crt_menu = db.query(Menu).filter(Menu.menu_id == menu_id).first() #current_menu
    return templates.TemplateResponse("edit_menu.html", {"request": request, "crt_menu": crt_menu})

@app.post("/edit/{menu_id}")
async def edit_menu(request: Request, menu_id: int, menu_nm: str = Form(...), kcal_g: int = Form(...), sacch_g: int = Form(...), protein_g: float = Form(...), sodium_mg: float = Form(...), sat_fat_g: int = Form(...), caffeine_mg: int = Form(...), category: str = Form(...), db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.menu_id == menu_id).first()
    menu.menu_nm = menu_nm
    menu.kcal_g = kcal_g
    menu.sacch_g = sacch_g
    menu.protein_g = protein_g
    menu.sodium_mg = sodium_mg
    menu.sat_fat_g = sat_fat_g
    menu.caffeine_mg = caffeine_mg
    menu.category = category
    db.commit()
    return RedirectResponse(url=app.url_path_for("load_db"), status_code=status.HTTP_303_SEE_OTHER)
    

@app.get("/del/{menu_id}")
async def del_menu(request: Request, menu_id: int, db: Session = Depends(get_db)):
    crt_menu = db.query(Menu).filter(Menu.menu_id == menu_id).first()
    db.delete(crt_menu)
    db.commit()
    return RedirectResponse(url=app.url_path_for("load_db"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/add")
async def add_menu(request: Request):
    return templates.TemplateResponse("add_menu.html", {"request":request})

@app.post("/add")
async def add_menu(menu_nm: str = Form(...), kcal_g: int = Form(...), sacch_g: int = Form(...), protein_g: float = Form(...), sodium_mg: float = Form(...), sat_fat_g: int = Form(...), caffeine_mg: int = Form(...), category: str = Form(...), db: Session = Depends(get_db)):
    menu = Menu()
    menu.menu_nm = menu_nm
    menu.kcal_g = kcal_g
    menu.sacch_g = sacch_g
    menu.protein_g = protein_g
    menu.sodium_mg = sodium_mg
    menu.sat_fat_g = sat_fat_g
    menu.caffeine_mg = caffeine_mg
    menu.category = category

    db.add(menu)
    db.commit()
    
    return RedirectResponse(url=app.url_path_for("load_db"), status_code=status.HTTP_303_SEE_OTHER)
