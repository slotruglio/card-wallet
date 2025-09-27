import os

from typing import Union
from fastapi import FastAPI

from .router.giftcard import router as giftcard_router

app = FastAPI()
app.include_router(giftcard_router, prefix="/giftcard")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/env")
def read_os_env():
    return os.environ


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}