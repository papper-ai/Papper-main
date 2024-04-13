from fastapi import APIRouter, Body, Form, UploadFile, Depends, File
from typing import List
from typing_extensions import Annotated
from ..schemas import Bibki
from dependencies import parse_jwt

router = APIRouter(prefix="/vault", tags=["Documents & Vaults"])


@router.post("/create_vault", dependencies=[Depends(parse_jwt)])
async def create_vaults(
    vault_name: Annotated[str, Form()],
    files: Annotated[List[UploadFile], File()],
):
    pass
