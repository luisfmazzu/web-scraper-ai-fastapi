import logging
from typing import Any

from pydantic import BaseSettings
from pymongo import MongoClient
from multiprocessing import Queue
from .logger import configure_structlog


class Config(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

    MONGO_DATABASE: str = "fastapi"
    MONGO_URL: str = ""

    OPEN_API_KEY: str = ""


# environmental variables
env = Config()

# FastAPI configurations
fastapi_config: dict[str, Any] = {
    "title": "API",
}

# MongoDB connection
client = MongoClient(env.MONGO_URL)

# MongoDB database
database = client[env.MONGO_DATABASE]

# Scrape Queue
scrape_queue = Queue()

# Logger
logging.basicConfig(level=logging.INFO)
configure_structlog()
