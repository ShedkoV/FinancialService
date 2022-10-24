"""Models for operations"""
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel# pylint: disable=no-name-in-module


class OperationKind(str, Enum):# pylint: disable=too-few-public-methods
    """Operation Kind Model"""
    INCOME = 'income'
    OUTCOME = 'outcome'


class BaseOperation(BaseModel):# pylint: disable=too-few-public-methods
    """Base Operation Model"""
    date: date
    kind: OperationKind
    amount: Decimal
    description: Optional[str]


class OperationCreate(BaseOperation):# pylint: disable=too-few-public-methods
    """Operation Create Model"""


class OperationUpdate(BaseOperation):# pylint: disable=too-few-public-methods
    """Operation Update Model"""


class Operation(BaseOperation):# pylint: disable=too-few-public-methods
    """Operation Model"""
    id: int

    class Config:# pylint: disable=too-few-public-methods
        """orm mode on"""
        orm_mode = True
