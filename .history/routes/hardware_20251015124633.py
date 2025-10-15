from fastapi import FastAPI, APIRouter, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil, os, uuid
import httpx  # để gửi dữ liệu lên web server
from websocket_manager import manager
from fastapi import APIRouter, Body
app = FastAPI(
    title="Fruit & Hardware API",
    description="API for managing fruits, hardware, and weights",
    version="1.0.0"
)

# Cho phép ESP8266 truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Router Hardware ---
router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"]
)

