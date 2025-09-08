
from fastapi import FastAPI
from routes import bills, fruits, users ,statistics   

app = FastAPI(
    title="Fruit Store API",
    description="API for managing fruits, users, bills",
    version="1.0.0"
)

# include routers
app.include_router(fruits.router)
app.include_router(users.router)
app.include_router(bills.router)
app.include_router(statistics.router)
# test root
@app.get("/")
def root():
    return {"message": "Welcome to Fruit Store API"}


