from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    groq_api_key: str
    model_name: str = "llama-3.3-70b-versatile"
    app_env: str = "development"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()