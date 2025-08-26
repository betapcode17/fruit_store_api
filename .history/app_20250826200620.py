from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

# Path parameter:
@app.get("/item/{item_id}")
def get_item(item_id:int):
    return {"item_id" : item_id}

#