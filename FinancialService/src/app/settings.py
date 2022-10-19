import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000

    database_url = "postgresql://{}:{}@localhost/fin_service".format(
        os.environ.get('DATABASE_USER'),
        os.environ.get("DATABASE_PASS")
    )

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 1 * 60 * 60

    class Config:
        orm_mode = True


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
