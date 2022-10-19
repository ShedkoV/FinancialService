from fastapi import (
    Depends,
    APIRouter,
    Response,
    HTTPException,
    status
)
from tables import User
from typing import Optional
from services.auth import get_current_user
from services.operations import OperationService
from models.operations import Operation, OperationKind, OperationCreate, OperationUpdate


router = APIRouter(
    prefix='/operations',
    tags=['Operations'],
)


@router.get('/', response_model=list[Operation])
def get_operations(
    kind: Optional[OperationKind] = None,
    user: User = Depends(get_current_user),
    service: OperationService = Depends(),

):
    return service.get_list(user_id=user.id, kind=kind)


@router.post('/', response_model=Operation)
def create_operation(
    operation_data: OperationCreate,
    user: User = Depends(get_current_user),
    service: OperationService = Depends(),
):
    return service.create(user_id=user.id, creation_data=operation_data)


@router.get('/{operation_id}', response_model=Operation)
def get_operation(
    operation_id: int,
    user: User = Depends(get_current_user),
    service: OperationService = Depends(),
):
    result = service.get(user_id=user.id, operation_id=operation_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


@router.put('/{operation_id}', response_model=Operation)
def update_operation(
    operation_id: int,
    operation_data: OperationUpdate,
    user: User = Depends(get_current_user),
    service: OperationService = Depends(),
):
    result = service.update(
        user_id=user.id, 
        operation_id=operation_id, 
        operation_data=operation_data
    )

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return result


@router.delete('/{operation_id}')
def delete_operation(
    operation_id: int,
    user: User = Depends(get_current_user),
    service: OperationService = Depends(),
):
    if not service.delete(user_id=user.id, operation_id=operation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
