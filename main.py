from typing import Annotated
from fastapi import FastAPI, Query
from enum import Enum
from pydantic import BaseModel


class ModelName(str, Enum):
    dawidnet = "dawidnet"
    tomeknet = "tomeknet"
    adinet = "adinet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


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


@app.get("/items")
async def read_items(
        query_item: Annotated[str, Query(
            alias="query-item",
            title="My requested query",
            description="This is just a simple query parameter",
            min_length=3,
            deprecated=True
        )
        ] = None):
    result = {"items": [
        {"item_id": "item_id1"}, {"item_id": "item_id2"}
    ]}
    if query_item:
        result.update({"q": query_item})
    return result


@app.get("/items/{item_id}")
async def read_item(item_id: int, needy: str, skip: int = 0, limit: int | None = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        end_price = item.price + item.tax
        item_dict.update({"end_price": end_price})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
