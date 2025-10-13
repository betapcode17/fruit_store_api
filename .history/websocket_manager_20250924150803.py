from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()
@app.websocket("/ws/weight")
async def websocket_weight(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Đọc trọng lượng từ Load Cell
            weight = hx.get_weight_mean(5)  # Lấy trung bình 5 lần đọc
            data = {"weight": weight}

            # Gửi dữ liệu tới client
            await websocket.send_json(data)
            
            await asyncio.sleep(0.5)  # Delay 0.5s, điều chỉnh tùy ý
    except WebSocketDisconnect:
        manager.disconnect(websocket)