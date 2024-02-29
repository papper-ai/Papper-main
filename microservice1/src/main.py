from fastapi import FastAPI

#from src.database.models import User  # пример импорта

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Bipka World"}
