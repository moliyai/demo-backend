from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from src.config import Config
from app.routes.v1 import router as V1Router

config = Config("configs/main.yaml").read()

app = FastAPI(
    title="demo-ai-service",
    version=config["fastapi"]["version"],
    debug=config["fastapi"]["debug"],
    docs_url=config["fastapi"]["doc_url"],
    openapi_url=config["fastapi"]["openapi_url"],
)

app.include_router(V1Router, prefix="/api")


BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = BASE_DIR / "uploads"


STATIC_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")