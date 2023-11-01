import cryptography # 이 라이브러리가 없으면 오류 발생

from fastapi import APIRouter, Depends, Form, status
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from math import ceil

from database import *
from models import *

from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="templates")

admin = APIRouter(prefix='/admin')
admin.mount("/static", StaticFiles(directory="statics"), name="static")
engine = engineconn()

def get_db():
    session = engine.session_maker()
    try:
        yield session
    finally:
        session.close()

def pagination_menu(db: Session, begin: int = 1, limit: int = 20):
    _dt_info = db.query(Menu).order_by(Menu.menu_id)

    total = _dt_info.count()
    dt_info = _dt_info.offset(begin).limit(limit).all()
    return total, dt_info

def pagination_fmenu(db: Session, begin: int = 1, limit: int = 20, categories: list = ["전체"]):
    _fdt_info = db.query(Menu).filter(Menu.category.in_(categories))

    total = _fdt_info.count()
    fdt_info = _fdt_info.offset(begin).limit(limit).all()

    return total, fdt_info

@admin.get("/", tags=['admin'])
async def load_db(request: Request, page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    total, dt_info = pagination_menu(db, begin=(page-1)*size, limit=size)
    total = ceil(total/size)

    return templates.TemplateResponse("db_test.html", {"request":request, "page":page, "size":size, "total":total, "dt_info":dt_info})

@admin.get("/?page={page}&size={size}", tags=['admin'])
async def load_db(request: Request, page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    total, dt_info = pagination_menu(db, begin=(page-1)*size, limit=size)
    total = ceil(total/size)

    return templates.TemplateResponse("db_test.html", {"request":request, "page":page, "size":size, "total":total, "dt_info":dt_info})

@admin.post("/", tags=['admin'])
async def filter_db(request: Request, page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    form_data = await request.form()
    categories = form_data.getlist("category")
    
    if categories:
        total, fdt_info = pagination_fmenu(db, begin=(page-1)*size, limit=size, categories=categories)
        total = ceil(total/size)
    
    if "전체" in categories or not categories:
        total, fdt_info = pagination_menu(db, begin=(page-1)*size, limit=size)
        total = ceil(total/size)
    

    return templates.TemplateResponse("db_test.html", {"request":request, "page":page, "size":size, "total":total, "dt_info":fdt_info})

@admin.get("/edit/{menu_id}", tags=['admin'])
async def edit_menu(request: Request, menu_id: int, db: Session = Depends(get_db)):
    crt_menu = db.query(Menu).filter(Menu.menu_id == menu_id).first() #current_menu
    return templates.TemplateResponse("edit_menu.html", {"request": request, "crt_menu": crt_menu})

@admin.post("/edit/{menu_id}", tags=['admin'])
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
    return RedirectResponse(url=admin.url_path_for("load_db"), status_code=status.HTTP_303_SEE_OTHER)
    

@admin.get("/del/{menu_id}", tags=['admin'])
async def del_menu(request: Request, menu_id: int, db: Session = Depends(get_db)):
    crt_menu = db.query(Menu).filter(Menu.menu_id == menu_id).first()
    db.delete(crt_menu)
    db.commit()
    return RedirectResponse(url=admin.url_path_for("load_db"), status_code=status.HTTP_303_SEE_OTHER)

@admin.get("/add", tags=['admin'])
async def add_menu(request: Request):
    return templates.TemplateResponse("add_menu.html", {"request":request})

@admin.post("/add", tags=['admin'])
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
    
    return RedirectResponse(url=admin.url_path_for("load_db"), status_code=status.HTTP_303_SEE_OTHER)