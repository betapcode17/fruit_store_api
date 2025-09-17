from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Fruit(Base):
    __tablename__ = "fruits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    quantity = Column(Integer, default=0) 
    image = Column(String(255))
    price = Column(Float, nullable=False)

    # Quan hệ 1-n với BillDetail
    bill_details = relationship("BillDetail", back_populates="fruit")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(50))
    address = Column(String(255))
    birth = Column(Date)
    gender = Column(Boolean) 
    username = Column(String(100), unique=True)
    role = Column(Boolean, default=True)  # để String cho linh hoạt
    valid = Column(Boolean, default=True)  

    # Quan hệ 1-n với Bill
    bills = relationship("Bill", back_populates="user")


class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow)  # <-- tự sinh thời gian tạo
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_cost = Column(Float, default=0)

    # Quan hệ
    user = relationship("User", back_populates="bills")
    bill_details = relationship("BillDetail", back_populates="bill", cascade="all, delete-orphan")


class BillDetail(Base):
    __tablename__ = "bill_details"

    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey("bills.bill_id"))
    fruit_id = Column(Integer, ForeignKey("fruits.id"))
    weight = Column(Float, nullable=False)
    price = Column(Float, nullable=False)  # giá tại thời điểm mua

    # Quan hệ
    bill = relationship("Bill", back_populates="bill_details")
    fruit = relationship("Fruit", back_populates="bill_details")
