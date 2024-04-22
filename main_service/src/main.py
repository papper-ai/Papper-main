from fastapi import FastAPI
import aiohttp
from contextlib import asynccontextmanager
from src.auth_service.api import auth_router
from src.vault_service.api import vault_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with aiohttp.ClientSession() as session:
        yield {"client_session": session}


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(vault_router)


@app.get("/")
async def hello():
    return {"message": "Hello from main service!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000)
