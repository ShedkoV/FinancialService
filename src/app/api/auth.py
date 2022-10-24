"""Api urls and views for users"""
from fastapi import Depends, APIRouter, status
from ..auth import UserCreate, Token, User
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import AuthService, get_current_user


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post(
    '/sign-up/',
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
def sign_up(
    user_data: UserCreate,
    auth_service: AuthService = Depends(),
):
    """Registration"""
    return auth_service.register_new_user(user_data)


@router.post(
    '/sign-in/',
    response_model=Token,
)
def sign_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    """Autorization"""
    return auth_service.authenticate_user(
        auth_data.username,
        auth_data.password,
    )


@router.get(
    '/user/',
    response_model=User,
)
def get_user(user: User = Depends(get_current_user)):
    """Getting one user"""
    return user
