# Managing Pydantic Data Models in FastAPI
# ----------------------------------------
# from pydantic import BaseModel, ValidationError, Field
# from enum import Enum
# from typing import List, Optional

# class Gender(str, Enum):
#     MALE = "MALE"
#     FEMALE = "FEMALE"
#     NON_BINARY = "NON_BINARY"

# class Person(BaseModel):
#     first_name: str
#     last_name: str
#     age: int
#     gender: Gender
#     interests: List[str]

# # Field validation
# # ----------------
# class Person(BaseModel):
#     first_name: str = Field(..., min_length=3)
#     last_name: str = Field(..., min_length=3)
#     age: Optional[int] = Field(None, ge=0, le=120)

# def validating_errors():
#     try:
#         Person(
#         first_name="Meghana",
#         last_name="Pgvhv",
#         gender="sd",
#         age="29",
#         interests=["coding", "movies"],
#         )
#     except ValidationError as e:
#         print(str(e))

# validating_errors()


# Dynamic default values
# ----------------------
# from datetime import datetime, date
# from typing import List
# from pydantic import BaseModel, Field, ValidationError

# def list_factory():
#     return ["a", "b", "c"]

# class Model(BaseModel):
#     l: List[str] = Field(default_factory=list_factory)
#     d: datetime = Field(default_factory=datetime.now)
#     l2: List[str] = Field(default_factory=list)

# def validating_errors():
#     try:
#         Model(
#         l=["ramesh", "nandish", "meghana"],
#         d="2022-02-12 12:09",
#         l2=["Meghana"]
#         )
#     except ValidationError as e:
#         print(str(e))

# validating_errors()

# Validating email addresses and URLs with Pydantic types
# -------------------------------------------------------
# pip install email-validator
# from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError

# class User(BaseModel):
#     email: EmailStr
#     website: HttpUrl

# def validating_errors():
#     try:
#         User(
#         email="kfj@gmail.com",
#         website="http://ksdfjlkjdfs.com")
#     except ValidationError as e:
#         print(str(e))

# validating_errors()

# Adding custom data validation with Pydantic
# --------------------------------------------
# --------------------------------------------
# Applying validation at a field level
# -------------------------------------
# from datetime import date
# from pydantic import BaseModel, validator


# class Person(BaseModel):
#     first_name: str
#     last_name: str
#     birthdate: date


#     @validator("birthdate")
#     def valid_birthdate(cls, v:date):
#         delta = date.today() - v
#         age = delta.days / 365
#         if age > 120:
#             raise ValueError("You seem a bit too old!")
#         return v

# def validating_errors():
#     Person(
#     first_name="John",
#     last_name="Doe",
#     birthdate="2000-10-08" # YYYY-MM-DD
#     )

# validating_errors()

# Applying validation at an object level
# --------------------------------------
# from pydantic import BaseModel, EmailStr, ValidationError, root_validator

# class UserRegisration(BaseModel):
#     email: EmailStr
#     password: str
#     password_confirmation: str
#     @root_validator()
#     def passwords_match(cls, values):
#         password = values.get("password")
#         password_confirmation = values.get("password_confirmation")
#         if password!=password_confirmation:
#             raise ValueError("Password don't match")
#         return values

# def validating_errors():
#     UserRegisration(
#     email="johngmail.com",
#     password="Doe",
#     password_confirmation="Doesfc" # YYYY-MM-DD
#     )

# validating_errors()


# Applying validation before Pydantic parsing
# -------------------------------------------
# from typing import List
# from pydantic import BaseModel, validator


# class Model(BaseModel):
#     values: List[int]
#     @validator("values", pre=True)
#     def split_string_values(cls, v):
#         if isinstance(v, str):
#             return v.split(",")
#         return v

# m = Model(values="1,2,3,4, hsh,")
# print(m.values)

# Converting an object into a dictionary
# --------------------------------------
# from datetime import date
# from pydantic import BaseModel, validator
# from enum import Enum
# from typing import List


# class Gender(str, Enum):
#     MALE = "MALE"
#     FEMALE = "FEMALE"
#     NON_BINARY = "NON_BINARY"


# class Person(BaseModel):
#     first_name: str
#     last_name: str
#     birthdate: date
#     interests: List[str]
#     gender: Gender


# person = Person(
#     first_name="John",
#     last_name="Doe",
#     gender=Gender.MALE,
#     birthdate="1991-01-01",
#     interests=["travel", "sports"],
#     )
# print(person)

# person_dict = person.dict()
# print(person_dict)
# print(person_dict.get('first_name'))
# print(person_dict['first_name'])
# person_include = person.dict(include={"first_name", "last_name"})
# print(person_include)
# person_exclude = person.dict(exclude={"first_name", "last_name"})
# print(person_exclude)


# ----------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# Dependency Injections in FastAPI
# --------------------------------
# from fastapi import FastAPI, Header


# app = FastAPI()


# @app.get("/")
# async def header(user_agent: str = Header(...)):
#     return {"user_agent": user_agent}


# Creating and using a parameterized dependency with a class
# -----------------------------------------------------------
# from typing import Tuple
# from fastapi import FastAPI, Depends, Query


# app = FastAPI()


# class Pagination:
#     def __init__(self, maximum_limit: int = 100):
#         self.maximum_limit = maximum_limit
#     def __call__(
#         self,
#         skip: int = Query(0, ge=0),
#         limit: int = Query(10, ge=0),
#         ) -> Tuple[int, int]:
#         capped_limit = min(self.maximum_limit, limit)
#         return (skip, capped_limit)


# pagination = Pagination(maximum_limit=50)
# @app.get("/items")
# def list_items(p: Tuple[int, int] = Depends(pagination)):
#     skip, limit = p
#     return {"skip": skip, "limit": limit}

# Use class methods as dependencies
# ----------------------------------
# from typing import Tuple
# from fastapi import FastAPI, Depends, Query


# app = FastAPI()


# class Pagination:
#     def __init__(self, maximum_limit: int = 100):
#         self.maximum_limit = maximum_limit
#     async def skip_limit(
#     self,
#         skip: int = Query(0, ge=0),
#         limit: int = Query(10, ge=0),
#           ) -> Tuple[int, int]:
#         capped_limit = min(self.maximum_limit, limit)
#         print(skip, capped_limit)
#         return (skip, capped_limit)
#     async def page_size(
#         self,
#         page: int = Query(1, ge=10),
#         size: int = Query(10, ge=1),
#         ) -> Tuple[int, int]:
#         capped_size = min(self.maximum_limit, size)
#         print(page, capped_size)
#         return (page, capped_size)


# pagination = Pagination(maximum_limit=50)

# @app.get("/items")
# async def list_items(p: Tuple[int, int] = Depends(pagination.skip_limit)):
#     skip, limit = p
#     return {"skip": skip, "limit": limit}


# @app.get("/things")
# async def list_things(p: Tuple[int, int] = Depends(pagination.page_size)):
#     page, size = p
#     return {"page": page, "size": size}

# Use a dependency on a whole router
# ----------------------------------
# from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Header
# from typing import Optional


# app = FastAPI()

# def secret_header(secret_header: Optional[str] = Header(None)) -> None:
#     if not secret_header or secret_header != "SECRET_VALUE":
#         raise HTTPException(status.HTTP_403_FORBIDDEN)

# # Use a dependency on a whole application
# # ----------------------------------------
# app = FastAPI(dependencies=[Depends(secret_header)])


# # Use a dependency on a path decorator
# # -------------------------------------
# @app.get("/protected-route", dependencies=[Depends(secret_header)])
# async def protected_route():
#     return {"hello": "world"}


# # Use a dependency on a whole router
# # ----------------------------------
# router = APIRouter(dependencies=[Depends(secret_header)])
# @router.get("/route1")
# async def router_route1():
#     return {"route": "route1"}
# @router.get("/route2")
# async def router_route2():
#     return {"route": "route2"}
# app = FastAPI()
# app.include_router(router, prefix="/router")


