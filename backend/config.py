import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-jwt-secret")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = FLASK_ENV == "development"

    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "criminal_id_system")


if not Config.MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable is not set")

mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client[Config.MONGO_DB_NAME]
