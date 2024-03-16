from fastapi import FastAPI
import aiohttp
from contextlib import asynccontextmanager
from .src import router as services_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with aiohttp.ClientSession() as session:
        yield {"client_session": session}


app = FastAPI(lifespan=lifespan)
app.include_router(services_router)

if __name__ == "__main__":
    uvicorn.run("main_service.main:app", host="0.0.0.0", port=8001, reload=True)
