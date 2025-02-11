from pydantic_settings import BaseSettings  # ✅ Use `pydantic_settings`
import os


class Settings(BaseSettings):
    # ✅ Get from environment variables
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    class Config:
        env_file = ".env"  # ✅ Load variables from .env file


# Create an instance of the settings
settings = Settings()
