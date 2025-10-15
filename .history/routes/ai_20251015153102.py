from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/api/upload_result")
async def upload_result(request: Request):
    data = await request.json()
    print("Received JSON:", data)
    # Lưu vào DB hoặc xử lý thêm ở đây
    return {"message": "JSON received successfully!"}