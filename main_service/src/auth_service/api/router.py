from fastapi import APIRouter, Depends, status
from typing import Annotated
from ..schemas import JWTTokensResponse, JWTRefreshRequest
from .dependencies import (
    authorize_user,
    register_user,
    get_new_tokens,
)

router = APIRouter(prefix="/auth", tags=["Authorization"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post(
    "/login",
    response_model=JWTTokensResponse,
    status_code=status.HTTP_200_OK,
)
async def login(jwt_tokens: Annotated[JWTTokensResponse, Depends(authorize_user)]):
    """
    На вход подаются данные в виде **HTML формы**.
    При успешной регистрации возвращаются 2 токена: access и refresh
    """
    return jwt_tokens


@router.post(
    "/registration",
    dependencies=[Depends(register_user)],
    status_code=status.HTTP_201_CREATED,
)
async def registration():
    """
    На вход подаются данные в виде **HTML формы**.
    При успешной регистрации возвращается статус 201
    """
    return {"message": "Successfully registered"}


@router.post(
    "/refresh_access_token",
    response_model=JWTTokensResponse,
)
async def refresh_tokens(
    jwt_tokens: Annotated[JWTRefreshRequest, Depends(get_new_tokens)]
):
    """
    На вход приходит refresh токен в теле запроса.
    При успешном обновлении возвращаются 2 токена: access и refresh.
    """
    return jwt_tokens
