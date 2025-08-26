from sqlalchemy import Column,Integer,String,Float,Date,
from .database import Base

class Fruit(Base):
    __tablename__ = "fruits"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    exist = Column(Float, default=0)
    image = Column(String(255))
    price = Column(Float, nullable=False)

class User(Base):
    id = Column(String(100),primary_key= True, index = True)
    email = Column(String(255),nullable= False)
    password = Column(String(255),nullable=False)
    name = Column(String(100), nullable= False)
    phone = Column(String(255))
    address = Column(String(255))
    birth = Column(Date)
    gender = Column()
    username = Column(String(255))
    role = (Column())
    valid = Column()

class Bill(Base):
    bill_id = Column(String())
    Date = Column()
    User_id = Column()
    Total_cost = Column()


class Bill_Detail(Base):
    detail_id = Column()
    Bill_id = Column()
    