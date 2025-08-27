from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import Fruit
from database import get_db
from schemas.fruits import FruitResponse, FruitCreate, FruitUpdate

router = APIRouter(
    prefix="/fruits",
    tags=["Fruits"]
)


# add new fruit
@router.post("/", response_model=FruitResponse)
def create_fruit(fruit_in: FruitCreate, db: Session = Depends(get_db)):
    fruit = Fruit(**fruit_in.dict())
    db.add(fruit)
    db.commit()
    db.refresh(fruit)
    return fruit


# get all fruits
@router.get("/", response_model=list[FruitResponse])
def list_fruits(db: Session = Depends(get_db)):
    return db.query(Fruit).all()


# delete fruit by id
@router.delete("/{fruit_id}")
def delete_fruit(fruit_id: int, db: Session = Depends(get_db)):
    fruit = db.query(Fruit).filter(Fruit.id == fruit_id).first()
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    db.delete(fruit)
    db.commit()
    return {"message": "Fruit deleted successfully"}


# update fruit
@router.put("/{fruit_id}", response_model=FruitResponse)
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
@router.get("/{fruit_id}", response_model=FruitResponse)
def detail_fruit(fruit_id: int, db: Session = Depends(get_db)):
    fruit = db.query(Fruit).filter(Fruit.id == fruit_id).first()
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return fruit


# search fruit by keyword
@router.get("/search", response_model=list[FruitResponse])
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
