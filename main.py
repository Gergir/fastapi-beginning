from fastapi import FastAPI
from enum import Enum

app = FastAPI()


# Path examples

class ModelName(str, Enum):
    dawidnet = "dawidnet"
    tomeknet = "tomeknet"
    adinet = "adinet"


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


# query examples
fake_items_db = [{'item_name': 'carrot'}, {'item_name': 'tomato'}, {'item_name': 'onion'}]


@app.get("/fake-items")
async def get_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# Note try: 127.0.0.1:8000/fake-items?skip=20


@app.get("/fake-items/{item_id}")
async def get_item(item_id: int, q: str | None = None, short_description: bool = False):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short_description:
        item.update({'description': 'This item contains a veeeery long description..'})
        print("Hola")
        print("Hola")
    return item


@app.get("users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: int, q: str | None = None, short: bool = True):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})

    if not short:
        item.update({'description': f'This items belongs to user with id {user_id}'})
    else:
        item.update({'description':f'item belongs to user: {user_id}'})
    return item

