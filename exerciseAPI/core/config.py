from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Exercise API"
    DATABASE_URL: str

    INTERNAL_SERVICE_URL: str

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return self.DATABASE_URL.replace("+asyncpg", "")

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = Extra.ignore


settings = Settings()
