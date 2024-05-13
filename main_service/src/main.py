from fastapi import FastAPI
import aiohttp
from contextlib import asynccontextmanager
from src.authorization.api import auth_router
from src.vaults.api import vault_router
from src.messaging.api import messaging_router
from src.rag.api import qa_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    timeout = aiohttp.ClientTimeout(total=120, connect=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        yield {"client_session": session}


app = FastAPI(lifespan=lifespan, title="Papper API", version="0.0.7", root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://172.20.0.2", "http://172.20.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(vault_router)
app.include_router(messaging_router)
app.include_router(qa_router)


@app.get("/")
async def hello():
    return {"message": "Hello from main service!"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        log_config="./uvicorn-logging-config.yaml",
    )
