# filename: app/core/config.py
import os

class Settings:
    PROJECT_NAME: str = "Klasstra"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://YOUR_DB_CONNECTION_STRING")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    RATE_LIMIT: int = 5 # announcements per minute per user

settings = Settings()
