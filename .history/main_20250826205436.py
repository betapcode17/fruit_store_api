# main.py
from database import Base, engine
from models import User, Fruit, Bill, BillDetail
# Tạo db nếu lần đầu
# def init_db():
#     print("Creating tables in database...")
#     Base.metadata.create_all(bind=engine)
#     print("Done!")

# if __name__ == "__main__":
#     init_db()



