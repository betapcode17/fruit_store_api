from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes import bills, fruits, users, statistics, hardware

# =========================
# WebSocket Manager
# =========================
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Client connected. Total:", len(self.active_connections))

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Client disconnected. Total:", len(self.active_connections))

    async def send_message_to_all(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# =========================
# FastAPI App
# =========================
app = FastAPI(
    title="Fruit Store API",
    description="API for managing fruits, users, bills",
    version="1.0.0"
)

# =========================
# Include Routers
# =========================
app.include_router(fruits.router)
app.include_router(users.router)
app.include_router(bills.router)
app.include_router(statistics.router)
app.include_router(hardware.router)

# =========================
# Root Endpoint
# =========================
@app.get("/")
def root():
    return {"message": "Welcome to Fruit Store API"}

# =========================
# WebSocket Endpoint
# =========================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print("Received from client:", data)
            # Optional: broadcast message to all clients
            await manager.send_message_to_all(f"Message from client: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

# =========================
# CORS Middleware
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dev only. In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
