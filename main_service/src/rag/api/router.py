from typing import Annotated
from ..schemas.qa import GenerationCredentials
import aiohttp
from fastapi import APIRouter, Depends
from src.dependencies import parse_jwt, get_aiohttp_session
from ..service import generate_answer
from src.messaging.schemas.history import AIMessage

router = APIRouter(prefix="/answer", tags=["QA"])


@router.post(
    "/generate_answer",
    response_model=AIMessage,
    dependencies=[Depends(parse_jwt)],
    description="Генерация ответа LLM",
)
async def answer_generation(
    generation_credentials: GenerationCredentials,
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> AIMessage:
    ai_message = await generate_answer(
        generation_credentials=generation_credentials,
        session=session,
    )

    return ai_message