# Create database if first
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
from database import get_db
app = FastAPI()



# add new fruit
@app.post("/addFruit")
def create_fruit(name: str,description:str, exist:bool,image:str,price:float,db: Session = Depends(get_db)):
   Fruit = Fruit(name = name , description = description, exist = exist,image = image,price = price)
   db.add(Fruit)
   db.commit()
   db.refresh(Fruit)
   return Fruit



# get all fruits


# delete fruit by id

#  update fruit inf

# get detail fruit by id

# find food