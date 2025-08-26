from sqlalchemy import Column,Integer,String,Float
from .database import Base

class Fruit(Base):
    __tablename__ = "fruits"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    exist = Column(Float, default=0)
    image = Column(String(255))
    price = Column(Float, nullable=False)

