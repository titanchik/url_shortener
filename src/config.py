from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@db:5432/postgres"
    redis_url: str = "redis://redis:6379"
    secret_key: str = "secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()