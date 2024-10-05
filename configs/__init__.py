from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: Optional[str] = "local"
    app_debug: Optional[bool] = True
    app_url: Optional[str]
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    encryption_key: str

    class Config:
        env_file = ".env"


settings = Settings()
