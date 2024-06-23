from typing import Annotated
from ..schemas.qa import GenerationCredentials, ModelAnswer
import aiohttp
from fastapi import APIRouter, Depends
from src.dependencies import parse_jwt_bearer, get_aiohttp_session
from ..service import generate_answer
from src.services.vaults.service.vaults import VaultsService
from src.services.vaults.api.dependencies import get_vaults_service
from src.services.messaging.service.messaging import MessagingService
from src.services.messaging.api.dependencies import get_messaging_service

router = APIRouter(prefix="/qa", tags=["QA"])


@router.post(
    "/generation",
    response_model=ModelAnswer,
    dependencies=[Depends(parse_jwt_bearer)],
    description="Генерация ответа LLM",
)
async def answer_generation(
    generation_credentials: GenerationCredentials,
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> ModelAnswer:
    ai_message = await generate_answer(
        generation_credentials=generation_credentials,
        messaging_service=messaging_service,
        vaults_service=vaults_service,
        session=session,
    )

    return ai_message
