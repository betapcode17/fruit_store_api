from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

# Path parameter:
@app.get("/item/{item_id}")
def get_item(item_id:int):
    return {"item_id" : item_id}

#Query parameter:
@app.get("/search")
def search(q: str = "default", limit: int = 10):
    return {"query": q, "limit": limit}