from ..schemas.tokens import JWTTokensResponse, AccessToken, RefreshToken


async def create_response_with_tokens(
    response: dict,
) -> JWTTokensResponse:
    access_token = AccessToken(token=response["access_token"])
    refresh_token = RefreshToken(token=response["refresh_token"])
    tokens = JWTTokensResponse(access_token=access_token, refresh_token=refresh_token)
    return tokens
