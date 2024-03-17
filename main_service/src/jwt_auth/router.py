from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Annotated
from .schemas import JWTTokensResponse, JWTRefreshRequest
from .dependencies import authorize_user, register_user, get_new_tokens

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get(
    "/login",
    description="login with particular user",
    response_model=JWTTokensResponse,
)
async def login(jwt_tokens: Annotated[JWTTokensResponse, Depends(authorize_user)]):
    """
    На вход подаются данные в виде формы (НЕ JSON)
    """
    return jwt_tokens


@router.post(
    "/registration",
    description="register new user",
    dependencies=[Depends(register_user)],
    status_code=status.HTTP_201_CREATED,
)
async def registration():
    """
    На вход подаются данные в виде **формы** (НЕ JSON)
    При успешной регистрации возвращается статус 201
    """
    return


@router.get(
    "/refresh_access_token",
    description="refresh access token via refresh token",
    response_model=JWTTokensResponse,
)
async def refresh_tokens(
    jwt_token: Annotated[JWTRefreshRequest, Depends(get_new_tokens)]
):
    return jwt_token
