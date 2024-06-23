from typing import Annotated
from ..schemas.qa import GenerationCredentials, ModelAnswer
import aiohttp
from fastapi import APIRouter, Depends
from src.dependencies import parse_jwt_bearer, get_aiohttp_session
from ..service import generate_answer

router = APIRouter(prefix="/qa", tags=["QA"])


@router.post(
    "/generation",
    response_model=ModelAnswer,
    dependencies=[Depends(parse_jwt_bearer)],
    description="Генерация ответа LLM",
)
async def answer_generation(
    generation_credentials: GenerationCredentials,
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> ModelAnswer:
    ai_message = await generate_answer(
        generation_credentials=generation_credentials,
        session=session,
    )

    return ai_message
