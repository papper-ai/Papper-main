from fastapi import FastAPI
import aiohttp
from contextlib import asynccontextmanager

client_session: aiohttp.ClientSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    global client_session
    client_session = aiohttp.ClientSession()
    yield
    await client_session.close()


app = FastAPI(lifespan=lifespan)
