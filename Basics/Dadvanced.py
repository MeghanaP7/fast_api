# Managing Authentication and Security in FastAPI
# ----------------------------------------------
# Security dependencies in FastAPI
# ---------------------------------
# 1. Basic HTTP authentication - user credentials (usually, an identifier such as an email address and password) are put into an HTTP header called Authorization.
# 2. Cookies - Cookies are a useful way to store static data on the client side
# 3. Tokens in the Authorization header - Probably the most used header in a REST API context, this simply consists of sending a token in an HTTP Authorization header.

# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.params import Depends
# from fastapi.security import APIKeyHeader
# API_TOKEN = "SECRET_API_TOKEN"


# app = FastAPI()


# api_key_header = APIKeyHeader(name="Token")


# @app.get("/protected-route")
# async def protected_route(token: str = Depends(api_key_header)):
#     if token != API_TOKEN:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
#     return {"hello": "world"}

# async def api_token(token: str = Depends(APIKeyHeader(name="Token"))):
#     if token != API_TOKEN:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

# @app.get("/protected-route", dependencies=[Depends(api_token)])
# async def protected_route():
#     return {"hello": "world"}

# Storing a user and their password securely in a database
# --------------------------------------------------------
import secrets
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr,Field
from datetime import datetime, timedelta
import sqlalchemy
from typing import Optional

from databases import Database
from passlib.context import CryptContext

# # Creating models and tables
app = FastAPI()

DATABASE_URL = "sqlite:///user_info.db"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_database() -> Database:
    return database


def get_password_hash(password: str) -> str:
    print(pwd_context.hash(password))
    return pwd_context.hash(password)
# # pip install fastapi aiosqlite email-validator databases passlib[bcrypt] python-multipart

database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)

class UserBase(BaseModel):
    email: EmailStr
class Config:
    orm_mode = True
class UserCreate(UserBase):
    password: str
class User(UserBase):
    id: int
class UserDB(User):
    hashed_password: str


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return datetime.now() + timedelta(seconds=duration_seconds)


class AccessToken(BaseModel):
    user_id: int
    access_token: str = Field(default_factory=generate_token)
    expiration_date: datetime = Field(default_factory=get_expiration_date)
class Config:
    orm_mode = True


metadata = sqlalchemy.MetaData()
user_info = sqlalchemy.Table(
"user_info",
metadata,
sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
sqlalchemy.Column("email", sqlalchemy.String(length=255), nullable=False),
sqlalchemy.Column("password", sqlalchemy.String(length=255), nullable=False)
)

access_token = sqlalchemy.Table(
"access_token",
metadata,
sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("user_info.id"), nullable=False),
sqlalchemy.Column("access_token", sqlalchemy.String(length=255), nullable=False),
sqlalchemy.Column("expiration_date", sqlalchemy.String(length=255), nullable=False)
)


@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# # Implementing registration routes
# # --------------------------------

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)

    try:
        db = get_database()
        insert_query = user_info.insert().values(email=user.email, password=hashed_password)
        await db.execute(insert_query)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid email")

# # Retrieving a user and generating an access token
# # ---------------------------------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate(email: str, password: str) -> Optional[UserDB]:
    try:
        db = get_database()
        print('before select query here', email, password)
        select_query = user_info.select().where(email==email)
        print('after select query here')
        result = await db.fetch_one(select_query)
        print('printing result', result)
        if result is None:
            return None

        if not verify_password(password, result[2]):
            return None
        # print("UserDB(**result)", UserDB(**result))
        # return UserDB(**result)
        return result
    except Exception as e:
        print(e.args[0])

async def create_access_token(user: UserDB) -> AccessToken:
    access_token_generated = AccessToken(user_id = user.id)
    print('access_token', access_token_generated.dict())
    access_token_generated_dict = access_token_generated.dict()
    db = get_database()
    insert_query = access_token.insert().values(access_token_generated.dict())
    result = await db.execute(insert_query)
    return access_token_generated_dict
    # print('AccessToken.from_orm(result) - ', AccessToken.from_orm(result))
    # return AccessToken.from_orm(result)


# # Implementing a login endpoint
# # --------------------------------

@app.post("/token")
async def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    email = form_data.username
    password = form_data.password
    user = await authenticate(email, password)
    print('user', user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = await create_access_token(user)
    print('token type ', type(token), token)
    return {
    "access_token": token['access_token'],
    "token_type": "bearer"
    }

# # Securing endpoints with access tokens
# # --------------------------------------

async def get_current_user(
    # token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")),
    token: str,):
    try:
        print('printing token - ', token)
        db = get_database()
        select_query = access_token.select().where(access_token.c.token==token)
        result = await db.fetch_one(select_query)
        print('result in get user', result)
        if result is None:
            return None

        return AccessToken(**result)

    except Exception as e:
        print(e.args[0])


async def get_user_info(id: int):
    try:

        db = get_database()
        select_query = user_info.select().where(user_info.c.id==id)
        result = await db.fetch_one(select_query)
        print('result in get user', result)
        if result is None:
            return None

        return result[1]

    except Exception as e:
        print(e.args[0])

@app.get("/protected-route")
async def protected_route(user: UserDB = Depends(get_current_user)):

    if user is None:
        return None
    print('user in protected route', user.dict())
    user_dict = user.dict()
    user_email_id = await get_user_info(user_dict['user_id'])
    user_dict['email'] = user_email_id
    return user_dict


