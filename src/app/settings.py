"""All settings"""
import os
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings


load_dotenv(find_dotenv())


class Settings(BaseSettings):# pylint: disable=too-few-public-methods
    """Set settings vars"""
    server_host: str = "127.0.0.1"
    server_port: int = 8000

    database_url = os.getenv("DATABASE_URL")

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 1 * 60 * 60

    class Config:# pylint: disable=too-few-public-methods
        """orm_mode on"""
        orm_mode = True


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
