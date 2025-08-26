# init_db.py
from database import Base, engine
from models import User, Fruit, Bill, BillDetail

print("Creating tables in database...")
Base.metadata.create_all(bind=engine)
print(" Done!")
