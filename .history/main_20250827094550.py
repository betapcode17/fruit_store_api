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
from schemas import FruitResponse,FruitCreate,FruitUpdate
app = FastAPI()



# add new fruit
@app.post("/addFruit", response_model=FruitResponse)
def create_fruit(fruit_in: FruitCreate, db: Session = Depends(get_db)):
    fruit = Fruit(**fruit_in.dict())
    db.add(fruit)
    db.commit()
    db.refresh(fruit)
    return fruit


# get all fruits
@app.get("/allFruits",response_class=list[FruitResponse])
def list_fruits(db: Session = Depends(get_db)):
    return db.query(Fruit).all()

# delete fruit by id


#  update fruit inf

# get detail fruit by id

# find food