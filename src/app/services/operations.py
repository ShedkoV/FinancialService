"""Business logic for operations"""
from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_session
from ..tables import Operation as table_operation
from ..models.operations import OperationKind, OperationCreate, OperationUpdate


class OperationService:
    """Operation Service"""
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_many(self, user_id: int) -> list[table_operation]:
        """get all operations by user"""
        operations = (
            self.session
            .query(table_operation)
            .filter(table_operation.user_id == user_id)
            .order_by(
                table_operation.date.desc(),
                table_operation.id.desc(),
            )
            .all()
        )
        return operations

    def _get(self, user_id: int, operation_id: int) -> table_operation:
        """get operation by id"""
        return (
            self.session
            .query(table_operation)
            .filter_by(
                id=operation_id,
                user_id=user_id,
            )
            .first()
        )

    def get_list(
        self,
        user_id: int,
        kind: Optional[OperationKind] = None) -> list[table_operation]:
        """get all operations"""
        query = (
            self.session
            .query(table_operation)
            .filter_by(user_id=user_id)
        )
        if kind:
            query = query.filter_by(kind=kind)

        return query.all()

    def get(self, user_id: int, operation_id: int) -> table_operation:
        """get operation"""
        return self._get(user_id, operation_id)

    def create_many(
        self,
        user_id: int,
        operations_data: list[OperationCreate]) -> list[table_operation]:
        """Creation operations report"""
        operations = [
            table_operation(
                **operation_data.dict(),
                user_id=user_id,
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)
        self.session.commit()

        return operations

    def create(self, user_id: int, creation_data: OperationCreate) -> table_operation:
        """Creation operation"""
        operation = table_operation(
            **creation_data.dict(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()

        return operation

    def update(
        self,
        user_id: int,
        operation_id: int,
        operation_data: OperationUpdate) -> table_operation:
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
