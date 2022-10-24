"""Models for user"""
from pydantic import BaseModel# pylint: disable=no-name-in-module


class BaseUser(BaseModel):# pylint: disable=too-few-public-methods
    """Base user model"""
    email: str
    username: str


class UserCreate(BaseUser):# pylint: disable=too-few-public-methods
    """User creat model"""
    password: str


class User(BaseUser):# pylint: disable=too-few-public-methods
    """User model"""
    id: int

    class Config:# pylint: disable=too-few-public-methods
        """orm mode on"""
        orm_mode = True


class Token(BaseModel):# pylint: disable=too-few-public-methods
    """Token model"""
    access_token: str
    token_type: str = 'bearer'
