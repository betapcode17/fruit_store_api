
from fastapi import FastAPI,websockets
from routes import bills, fruits, users ,statistics ,hardware  
from websocket_manager import 
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
app.include_router(hardware.router)
# test root
@app.get("/")
def root():
    return {"message": "Welcome to Fruit Store API"}


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # client có thể gửi "ping"
    except:
        manager.disconnect(websocket)