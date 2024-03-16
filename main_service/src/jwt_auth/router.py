from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import JWTResponse
from typing import Annotated
from main_service.main import client_session

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(data_form=Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = data_form.username
    password = data_form.password
    secret = data_form.secret
    async with client_session.post(...) as response:
        ...
    return response
