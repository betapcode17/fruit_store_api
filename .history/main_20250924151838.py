
from fastapi import FastAPI,WebSocket
from routes import bills, fruits, users ,statistics ,hardware 
from fastapi.middleware.cors import CORSMiddleware 
from websocket_manager import manager
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
            await websocket.receive_text()  
    except:
        manager.disconnect(websocket)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # hoặc ["*"] để test
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)       