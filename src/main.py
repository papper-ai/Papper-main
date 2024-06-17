from fastapi import FastAPI
import aiohttp
from contextlib import asynccontextmanager
from src.authorization.api import auth_router
from src.vaults.api import vault_router
from src.messaging.api import messaging_router
from src.rag.api import qa_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(url="redis://papper-main-redis:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    timeout = aiohttp.ClientTimeout(total=120, connect=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        yield {"client_session": session}


app = FastAPI(lifespan=lifespan, title="Papper API", version="0.0.7", root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(vault_router)
app.include_router(messaging_router)
app.include_router(qa_router)


@app.get("/")
@cache(expire=60)
async def hello():
    return {"message": "Hello from Main service!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        log_config="./uvicorn-logging-config.yaml",
    )
