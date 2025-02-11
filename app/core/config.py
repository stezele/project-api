from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"  # Read environment variables from the .env file


settings = Settings()
