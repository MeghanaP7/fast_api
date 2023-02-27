from fastapi import APIRouter
from db import get_database
from fastapi import status, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from models.model import contact_form

router = APIRouter()


class ContactForm(BaseModel):
    id: int
    name: str
    mobile: str
    email: EmailStr
    message: str
    created_date: datetime
    browser_type: str

class ContactFormPartialUpdate(BaseModel):
    id: int
    name: str
    mobile: str
    browser_type: str

@router.post("/contact_form", status_code=status.HTTP_201_CREATED)
async def data(user: ContactForm):
    try:
        db = get_database()
        insert_query = contact_form.insert().values(id=user.id,
                                                    name=user.name,
                                                    mobile=user.mobile,
                                                    email=user.email,
                                                    message=user.message,
                                                    created_date=user.created_date,
                                                    browser_type=user.browser_type
                                                    )

        await db.execute(insert_query)
        #print(insert_query)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='enter valid details')


@router.get("/contact_form")
async def retrieve_contact_form():
    db = get_database()
    select_query = contact_form.select()
    result = await db.fetch_all(select_query)
    return result


@router.get("/contact_form/{id}")
async def get_contact_form(id: int):
    try:
        db = get_database()
        select_query = contact_form.select().where(contact_form.c.id == id)
        result = await db.fetch_one(select_query)
        if result is None:
            return None
        return result
    except Exception as e:
        print(e.args[0])

@router.delete("/contact_form/{id}", status_code=status.HTTP_200_OK)
async def delete_contact_form(id: int):
    try:
        db = get_database()
        delete_query = (contact_form.delete().where(contact_form.c.id == id))
        result = await db.fetch_all(delete_query)
        return result
    except Exception as e:
        print(e.args[0])
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='successfully deleted')

@router.put("/contact_form/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_contact_form(id: int, user: ContactForm):
    try:
        db=get_database()
        update_query = (contact_form.update().where(contact_form.c.id == id).values(id=user.id,
                                                                                    name=user.name,
                                                                                    mobile=user.mobile,
                                                                                    email=user.email,
                                                                                    message=user.message,
                                                                                    created_date=user.created_date,
                                                                                    browser_type=user.browser_type
                                                                                    ))                              
        result = await db.fetch_one(update_query)
        if result is None:
            return None
        return result
    except Exception as e:
        print(e.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='enter valid details')

@router.patch("/contact_form/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_contact_form(id: int, user: ContactFormPartialUpdate):
    try:
        db = get_database()
        update_query =(contact_form.update().where(contact_form.c.id == id).values(
                                                                                    id= user.id,
                                                                                    name=user.name,
                                                                                    mobile=user.mobile,
                                                                                    browser_type=user.browser_type,
                                                                                    ))                                                                 
        result = await db.fetch_one(update_query)
        if result is None:
            return None
        return result
    except Exception as e:
        print(e.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='enter valid details')    
