from src.shared import ml_models
from ..messaging.schemas.history import UserMessageResponse, AIMessageResponse


async def truncate_history(
    history: list[UserMessageResponse | AIMessageResponse | None], max_tokens=7000
):
    tokenizer = ml_models["tokenizer"]
    tokens = 0
    for i in range(len(history) - 1, -1, -1):
        tokens += len(tokenizer(history[i].content).input_ids)
        if tokens >= max_tokens:
            return history[i + 1 :]

    return history  # Return the original list if sum does not exceed max_tokens
