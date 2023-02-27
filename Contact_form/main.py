import sqlalchemy
from fastapi import FastAPI
from db import database
from models.model import metadata
from routes.route import router


app = FastAPI()


DATABASE_URL = "sqlite:///Contact_form.db"

sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

metadata.create_all(sqlalchemy_engine)
app.include_router(router, prefix="")
