# Tạo db nếu lần đầu
# from database import Base, engine
# from models import User, Fruit, Bill, BillDetail
# def init_db():
#     print("Creating tables in database...")
#     Base.metadata.create_all(bind=engine)
#     print("Done!")
# if __name__ == "__main__":
#     init_db()
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from models import User,Fruit,Bill,BillDetail

app = FastAPI()



# them quả mới
@app.post("/addFruit")
def create_fruit(name: str,description)




# Lấy danh sách quả


# Xóa quả theo ID.

#  Cập nhật thông tin quả

# Lấy chi tiết quả theo ID

# Tìm quả theo tên chứa chuỗi