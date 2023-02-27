from fastapi import APIRouter
from models.model import person
from db import get_database

router = APIRouter()

@router.post("/person", tags=["Person"])
async def insert_person(name, city, salary):
    insert_stmt = person.insert().values(name=name, city=city, salary=salary)
    database = get_database()
    await database.execute(insert_stmt)
    return {
    "name": name,
    "city": city,
    "salary": salary
    }

@router.get("/person-data")
async def retrieve_person():
    select_stmt = person.select()
    result = await get_database().fetch_all(select_stmt)
    return result