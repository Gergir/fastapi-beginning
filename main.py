from typing import Annotated
from fastapi import FastAPI, Query, Path, Body
from enum import Enum
from pydantic import BaseModel, Field


class ModelName(str, Enum):
    dawidnet = "dawidnet"
    tomeknet = "tomeknet"
    adinet = "adinet"


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The amount of money the item cost")
    tax: float | None = None


class User(BaseModel):
    username: str
    full_username: str | None = None


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


@app.get("/items/{item_id}")
async def read_items(
        item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=100)],
        q: str | None = None,
        size: Annotated[float, Query(gt=0, le=10.4)] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results


@app.get("/users/me")
async def read_current_user():
    return {"user_id": "current_user_id"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, needy: str, skip: int = 0, limit: int | None = None):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item


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


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        end_price = item.price + item.tax
        item_dict.update({"end_price": end_price})
    return item_dict


# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=100)],
#         q: str | None = None,
#         size: Annotated[float | None, Query(gt=0, le=10.4)] = None,
#         item: Item | None = None):
#
#     result = {"item_id": item_id}
#     if q:
#         result.update({"q": q})
#     if size:
#         result.update({"size": size})
#     if item:
#         result.update({"item": item})
#     return result

@app.put("/items/{item_id}")
async def update_item(item_id: int,
                      item: Item,
                      user: User,
                      importance: Annotated[int | None, Body(ge=1)]
                      ):
    result = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return result
