# filename: app/core/config.py
import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Klasstra"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://YOUR_DB_CONNECTION_STRING")
    
    # If JWT_SECRET is not provided, generate one securely.
    jwt_secret_env = os.getenv("JWT_SECRET")
    if not jwt_secret_env or jwt_secret_env.strip() == "":
        # Generate a 43-character URL-safe secret (≈256 bits)
        jwt_secret_env = secrets.token_urlsafe(32)
        
    JWT_SECRET: str = jwt_secret_env
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    RATE_LIMIT: int = 5 # announcements per minute per user

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")


settings = Settings()
