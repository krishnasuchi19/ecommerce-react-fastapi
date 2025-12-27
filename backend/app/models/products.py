from sqlalchemy import Column, Integer, String, Float, Boolean
from .base import Base

class Products(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = True)
    description = Column(String)
    price = Column(Float, nullable = False)
    stock = Column(Integer, default = 0)
    is_active = Column(Boolean, default = True)