"""Business logic for operations"""
from typing import Optional
from fastapi import Depends
from database import get_session
from sqlalchemy.orm import Session
from models.operations import OperationKind, OperationCreate, OperationUpdate

import tables


class OperationService:
    """Operation Service"""
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_many(self, user_id: int) -> list[tables.Operation]:
        """get all operations by user"""
        operations = (
            self.session
            .query(tables.Operation)
            .filter(tables.Operation.user_id == user_id)
            .order_by(
                tables.Operation.date.desc(),
                tables.Operation.id.desc(),
            )
            .all()
        )
        return operations

    def _get(self, user_id: int, operation_id: int) -> tables.Operation:
        """get operation by id"""
        return (
            self.session
            .query(tables.Operation)
            .filter_by(
                id=operation_id,
                user_id=user_id,
            )
            .first()
        )

    def get_list(self, user_id: int, kind: Optional[OperationKind] = None) -> list[tables.Operation]:
        """get all operations"""
        query = (
            self.session
            .query(tables.Operation)
            .filter_by(user_id=user_id)
        )
        if kind:
            query = query.filter_by(kind=kind)
        
        return query.all()

    def get(self, user_id: int, operation_id: int) -> tables.Operation:
        """get operation"""
        return self._get(user_id, operation_id)

    def create_many(self, user_id: int, operations_data: list[OperationCreate]) -> list[tables.Operation]:
        """Creation operations report"""
        operations = [
            tables.Operation(
                **operation_data.dict(),
                user_id=user_id,
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)
        self.session.commit()
        
        return operations 

    def create(self, user_id: int, creation_data: OperationCreate) -> tables.Operation:
        """Creation operation"""
        operation = tables.Operation(
            **creation_data.dict(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()
        
        return operation

    def update(self, user_id: int, operation_id: int, operation_data: OperationUpdate) -> tables.Operation:
        """Edit operations"""
        operation = self._get(user_id, operation_id)
        if operation:
            for field, value in operation_data:
                setattr(operation, field, value)
            self.session.commit()
        
        return operation

    def delete(self, user_id: int, operation_id: int):
        """Delete operation"""
        operation = self._get(user_id, operation_id)
        if operation:
            self.session.delete(operation)
            self.session.commit()
            operation = True

        return operation
