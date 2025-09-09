from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List


app = FastAPI()

class ConnectionManger:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(WebSocket)

    def disconnect(self,websocket: WebSocket):
        self.active_connections.remove(WebSocket)

    async def broadcast(self, message : dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManger()

#
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:

            data = await websocket.receive_text()
            print(f"Message from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")