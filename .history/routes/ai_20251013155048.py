from fastapi import FastAPI, APIRouter, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil, os, uuid
import httpx  # để gửi dữ liệu lên web server
from websocket_manager import manager