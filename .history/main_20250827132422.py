# Create database if first
# from database import Base, engine
# from models import User, Fruit, Bill, BillDetail
# def init_db():
#     print("Creating tables in database...")
#     Base.metadata.create_all(bind=engine)
#     print("Done!")
# if __name__ == "__main__":
#     init_db()
# uvicorn main:app --reload chay du an

from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from models import User,Fruit,Bill,BillDetail
from database import get_db
from schemas import FruitResponse,FruitCreate,FruitUpdate
from sqlalchemy import or_
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
@app.get("/allFruits",response_model=list[FruitResponse])
def list_fruits(db: Session = Depends(get_db)):
    return db.query(Fruit).all()

# delete fruit by id
@app.delete("/deleteFruit/{fruit_id}")
def delete_fruit(fruit_id:int,db: Session = Depends(get_db)):
    fruit = db.query(Fruit).filter(Fruit.id == fruit_id).first()
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    db.delete(fruit)
    db.commit()
    return {"message" : "Fruit deleted successfully"}


#  update fruit inf
@app.post("/updateFruit/{fruit_id}", response_model=FruitResponse)
def update_fruit(fruit_id: int, fruit_in: FruitUpdate, db: Session = Depends(get_db)):
    fruit = db.query(Fruit).filter(Fruit.id == fruit_id).first()
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    for key, value in fruit_in.dict(exclude_unset=True).items():
        setattr(fruit, key, value)
    db.commit()
    db.refresh(fruit)
    return fruit



# get detail fruit by id
@app.get("/viewFruit/{fruit_id}",response_model=FruitResponse)
def detail_fruit(fruit_id:int, db: Session = Depends(get_db)):
    fruit = db.query(Fruit).filter(Fruit.id == fruit_id).first()
    if not fruit:
         raise HTTPException(status_code=404, detail="Fruit not found")
    return fruit



# find food by keyword
@app.get("/searchFruit",response_model=list[FruitResponse])
def search_fruit(keyword: str, db: Session = Depends(get_db)):
    fruits = db.query(Fruit).filter(
        or_(
            Fruit.name.ilike(f"%{keyword}%"),
            Fruit.description.ilike(f"%{keyword}%")
        )
    ).all()

    if not fruits:
        raise HTTPException(status_code=404, detail="No fruits found")

    return fruits



# register


#login


#view profile


#view all profile


#update profile


# change pass