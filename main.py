from fastapi import FastAPI
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
