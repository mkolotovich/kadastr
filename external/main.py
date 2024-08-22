from typing import Union
from typing import Annotated
from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.routing import Route
import requests

app = FastAPI()

@app.get("/")
async def show_main():
    return {"msg": "external server start"}

@app.post("/")
async def read_item(number: Annotated[int, Form()], latitudes: Annotated[float, Form()], longitude: Annotated[float, Form()]):
    if (-90 <= latitudes <= 90):
        print('true')
        return True
    print('false')
    return False