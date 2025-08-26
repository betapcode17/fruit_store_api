from sqlalchemy import Column,Integer,String,Float
from .database import Base

class Fruit(Base):
    __tablename__ = "fruits"

    