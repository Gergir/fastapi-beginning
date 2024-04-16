from fastapi import FastAPI
from enum import Enum


class ModelName(str, Enum):
    dawidnet = "dawidnet"
    tomeknet = "tomeknet"
    adinet = "adinet"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome in FastAPI"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.dawidnet:
        return {"model_name": model_name, "message": "Dawid"}
    if model_name == ModelName.adinet:
        return {"model_name": model_name, "message": "Adi"}

    return {"model_name": model_name, "message": "Tomek"}


@app.get("/users/me")
async def read_current_user():
    return {"user_id": "current_user_id"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
