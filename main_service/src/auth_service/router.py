from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Annotated
from .schemas import JWTTokensResponse, JWTRefreshRequest
from .dependencies import authorize_user, register_user, get_new_tokens

router = APIRouter(prefix="/auth", tags=["auth"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post(
    "/login",
    response_model=JWTTokensResponse,
)
async def login(jwt_tokens: Annotated[JWTTokensResponse, Depends(authorize_user)]):
    """
    На вход подаются данные в виде HTML формы, **подаете только логин и пароль**

    При успешной регистрации возвращаются 2 токена: access и refresh
    Находиться они будут либо в теле
    """
    return jwt_tokens


@router.get(
    "/registration",
    dependencies=[Depends(register_user)],
    status_code=status.HTTP_201_CREATED,
)
async def registration():
    """
    На вход подаются данные в виде HTML **формы** (НЕ JSON)
    При успешной регистрации возвращается статус 201
    """
    return


@router.post(
    "/refresh_access_token",
    response_model=JWTTokensResponse,
)
async def refresh_tokens(
    jwt_token: Annotated[JWTRefreshRequest, Depends(get_new_tokens)]
):
    """
    На вход приходит refresh токен в заголовке `Authorization: Bearer <token>`

    При успешном обновлении токенов возвращаются 2 токена: access и refresh.
    Находиться они будут либо в теле
    """
    return jwt_token
