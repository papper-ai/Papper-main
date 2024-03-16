from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from typing import Annotated
from .schemas import JWTTokensResponse, JWTRefreshRequest
from .dependencies import authorize_user, register_user, get_new_tokens

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
http_bearer = HTTPBearer()


@router.get(
    "/login",
    description="login with particular user",
    response_model=JWTTokensResponse,
)
async def login(tokens: Annotated[JWTTokensResponse, Depends(authorize_user)]):
    return tokens


@router.post(
    "/registration",
    description="register new user",
    dependencies=[Depends(register_user)],
)
async def registration():
    return


@router.get(
    "/refresh_access_token",
    description="refresh access token via refresh token",
    response_model=JWTTokensResponse,
)
async def refresh_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    request: Request,
):
    token = JWTRefreshRequest(refresh_token=credentials.credentials)
    tokens = await get_new_tokens(token=token, request=request)
    return tokens
