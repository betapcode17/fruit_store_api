
from fastapi import FastAPI
from routes import fruits, users    

app = FastAPI(
    title="Fruit Store API",
    description="API for managing fruits, users, bills",
    version="1.0.0"
)

# include routers
app.include_router(fruits.router)
app.include_router(users.router)
# test root
@app.get("/")
def root():
    return {"message": "Welcome to Fruit Store API"}


