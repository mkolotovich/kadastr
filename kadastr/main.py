import starlette.status as status
import psycopg2
from typing import Union
from typing import Annotated
from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.routing import Route
import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DeclarativeBase = declarative_base()

class Kadastr(DeclarativeBase):
    __tablename__ = 'kadastr'

    id = Column(Integer, primary_key=True)
    number = Column('number', Integer)
    latitudes = Column('latitudes', REAL)
    longitude = Column('longitude', REAL)
    answer = Column('answer', String)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

templates = Jinja2Templates(directory='templates')

engine = create_engine(url = DATABASE_URL, echo=True)

DeclarativeBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

async def read_root(request):
    return templates.TemplateResponse(request, 'index.html')

routes = [
    Route('/', endpoint=read_root),
]

app = FastAPI(routes=routes)

@app.post("/query")
async def read_item(request: Request, number: Annotated[int, Form()], latitudes: Annotated[float, Form()], longitude: Annotated[float, Form()]):
    response = requests.post('http://127.0.0.1:8000/', data={"number": number, "latitudes": latitudes, "longitude": longitude}, timeout=60)
    new_item = Kadastr(number=number, latitudes=latitudes, longitude=longitude, answer=response.text)
    session.add(new_item)
    session.commit()
    print(response.text)
    new_url = f"/result?param={response.text}"
    return RedirectResponse(url=new_url, status_code=303)

@app.get("/result")
async def give_result(param):
    return {"msg": param}

@app.get("/ping")
async def test_server():
    return {"msg": "Service is working"}

@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request):
    print(session.query(Kadastr.id, Kadastr.number, Kadastr.latitudes, Kadastr.longitude, Kadastr.answer).all())
    result = session.query(Kadastr.id, Kadastr.number, Kadastr.latitudes, Kadastr.longitude, Kadastr.answer).all()
    return templates.TemplateResponse(
        request=request, name="history.html", context={"result": result}
    )

@app.get("/history/{kadastr_number}", response_class=HTMLResponse)
async def get_history_by_num(request: Request, kadastr_number):
    print(session.query(Kadastr.id, Kadastr.number, Kadastr.latitudes, Kadastr.longitude, Kadastr.answer).filter(Kadastr.number == kadastr_number).all())
    result = session.query(Kadastr.id, Kadastr.number, Kadastr.latitudes, Kadastr.longitude, Kadastr.answer).filter(Kadastr.number == kadastr_number).all()
    return templates.TemplateResponse(
        request=request, name="history_by_num.html", context={"result": result}
    )
