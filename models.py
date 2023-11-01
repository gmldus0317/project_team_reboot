from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List, Optional

Base = declarative_base()

class Menu(Base):
    __tablename__="menu"

    menu_id = Column(Integer, primary_key=True)
    menu_nm = Column(String, nullable=False)
    kcal_g = Column(Integer, nullable=False)
    sacch_g = Column(Integer, nullable=False)
    protein_g = Column(Float, nullable=False)
    sodium_mg = Column(Float, nullable=False)
    sat_fat_g = Column(Integer, nullable=False)
    caffeine_mg = Column(Integer, nullable=False)
    category = Column(String, nullable=False)

    def __repr__(self):
        return '<Info %r>' % (self.menu_id)

class Cart_list(BaseModel):
    name: str