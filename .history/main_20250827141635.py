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

from fastapi import FastAPI
from routes import fruits, users

app = FastAPI(
    title="Fruit Store API",
    description="API for managing fruits, users, bills",
    version="1.0.0"
)

# include routers
app.include_router(fruits.router)

# test root
@app.get("/")
def root():
    return {"message": "Welcome to Fruit Store API"}


