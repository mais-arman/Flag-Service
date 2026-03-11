import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = 60

    DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")    