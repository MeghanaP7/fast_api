# FastAPI
# -------
# Backend + Frontend = Full Stack Development

# FastAPI + React JS = FARM Stack


# Python has got 3 different libraries / Frameworks to work with Web Development

# Flask- synchronous
# Django- synchronous
# FastAPI- asynchronous- faster application performance


# from fastapi import FastAPI

# # Creating instance of an FastAPI. app is an FastAPI object
# app = FastAPI()


# @app.get("/meghana") # get is a http method and / is a route
# def hello_world():
#     return {"hello": "meghana"}

# Handling request parameters
# ---------------------------
# from fastapi import FastAPI
# app = FastAPI()


# # Path parameters
# # ------------------
# @app.get("/users/{id}")
# def get_user(id: int):
#     return {"id": id}


# Limiting allowed values
# ------------------------
# from fastapi import FastAPI
# app = FastAPI()

# # User type can be the following
# # admin
# # standard
# # staff
# # superuser
# # manager

# from enum import Enum
# class UserType(str, Enum):
#     STANDARD = "standard"
#     ADMIN = "admin"
#     STAFF = "staff"
#     SUPERUSER = "superuser"
#     MANAGER = "manager"

# @app.get("/users/{type}/{id}/")
# async def get_user(type: str, id: int):
#     return {"type": type, "id": id}

# @app.get("/users/{type}/{id}/")
# def get_user(type: UserType, id: int):
#     return {"type": type, "id": id}


# Advanced validation
# -------------------
# gt: Greater than
# ge: Greater than or equal to
# lt: Less than
# le: Less than or equal to
# from fastapi import FastAPI, Path
# app = FastAPI()

# @app.get("/users/{age}")
# def get_user_age(age: int):
#     if age>=0 and age<=120:
#         return {"message": "you have correct age"}
#     return {"message": "you do not have correct age"}

# def get_user_age(age: int = Path(...,ge=20)):
#     return {"age": age}


# Query parameters
# ----------------
# from fastapi import FastAPI
# app = FastAPI()

# @app.get("/users")
# def get_user(page: int = 1, size: int = 10):
#     return {"page": page, "size": size}


# The request body
# ----------------
# from fastapi import FastAPI, Body
# app = FastAPI()

# @app.post("/users")
# def create_user(name: str = Body(...), age: int = Body(...)):
#     return {"name": name, "age": age}
# def create_user(name: str = Body(default="meghana"), age: int = Body(...)):
#     return {"name": name, "age": age}


# Pydantic models for data validation
# -----------------------------------
# Pydantic is a Python library for data validation and is based on classes and type hints.

# {
# "name":"Yaanavi",
# "age": 2
# }
# from fastapi import FastAPI
# from pydantic import BaseModel

# class User(BaseModel):
#     name: str
#     age: int


# app = FastAPI()
# @app.post("/users")
# def create_user(user: User):
#     return user



# Multiple objects
# -----------------
# from fastapi import FastAPI
# from pydantic import BaseModel

# class User(BaseModel):
#     name: str
#     age: int

# class Company(BaseModel):
#     name: str
#     year_of_establishment: int


# app = FastAPI()
# @app.post("/users")
# async def create_user(user: User, company: Company):
#     return {"user": user, "company": company}

# # {
# # "user": {
# # "name": "meghana",
# # "age": 29
# # },
# # "company": {
# # "name": "jpr inc",
# # "year_of_establishment": 2016
# # }
# # }

# Form data
# ---------
# pip install python-multipart

# from fastapi import FastAPI, Form

# app = FastAPI()

# @app.post("/users")
# def create_user(name: str = Form(...), age: int = Form(...)):
#     return {
#     "name": name,
#     "age": age
#     }

# File uploads
# -------------
# from fastapi import FastAPI, File
# app = FastAPI()
# @app.post("/files")
# def upload_file(file: bytes = File(...)):
# # list1 = [1, 3 , 6, 5]
# # return len(list1)
#     file_size = str(len(file)) + " - bytes"
#     return {
#     "file_size": file_size
#     }

# File type and file name
# -----------------------
# from fastapi import FastAPI, File, UploadFile
# app = FastAPI()
# @app.post("/files")
# def upload_file(file: UploadFile = File(...)):
#     return {
#     "file_name": file.filename,
#     "file_type": file.content_type
#     }


# Upload multiple files
# ---------------------
# from fastapi import FastAPI, File, UploadFile
# from typing import List, Dict, Tuple
# app = FastAPI()
# @app.post("/files")
# async def upload_multiple_files(files: List[UploadFile] = File(...)):
#     return [
#     {
#     "file_name": file.filename,
#     "content_type": file.content_type
#     }
#     for file in files
#     ]


# Headers
# --------
# from fastapi import FastAPI, Header
# app = FastAPI()

# @app.get("/header")
# def get_header(hello: str = Header(...)):
#     return {
#     "Hello": hello
#     }



# The request object
# -------------------
# object
# {
# "name": "Reshma"
# }

# from fastapi import FastAPI, Request
# app = FastAPI()
# @app.get("/request_object")
# def get_request_object(request: Request):
#     body_content = request.body
#     return {
#     "path": request.url.path,
#     "body": body_content
#     }

# Customizing the response
# -------------------------
# from fastapi import FastAPI, status
# from pydantic import BaseModel
# class Post(BaseModel):
#     title: str

# app = FastAPI()

# @app.post("/posts", status_code=status.HTTP_200_OK)
# def create_post(post: Post):
#     return post

# The response model
# ------------------
# from fastapi import FastAPI
# from pydantic import BaseModel

# class Post(BaseModel):
#     title: str
#     nb_views: int

# class PublicPost(BaseModel):
#     title: str

# app = FastAPI()

# # Dummy Database
# posts = {
# 1:Post(title="Hello", nb_views=100),
# 3:Post(title="World", nb_views=100)
# }

# @app.get("/posts/{id}")
# def get_post(id: int):
# return posts[id]


# @app.get("/posts/{id}", response_model=PublicPost)
# def get_post(id: int):
#     return posts[id]


# The response parameter
# -----------------------
# from fastapi import FastAPI, Response

# app = FastAPI()


# @app.get("/posts")
# def custom_header(response: Response):
# # response.headers["Custom-Header"] = "Meg"
#     response.set_cookie("cookie-name", "cookie-value", max_age=86400)
#     return {"hello": "world"}


# Raising HTTP errors
# -------------------
# from fastapi import FastAPI, Body, HTTPException, status

# app = FastAPI()

# @app.post("/password")
# def check_password(password: str = Body(...), confirm_password: str = Body(...)):
#     if password != confirm_password:
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Password Don't match")
#     return {"message": "Passwords match"}
# raise HTTPException(status.HTTP_400_BAD_REQUEST,detail={"message": "Passwords don't match.","hints": ["Check the caps lock on your keyboard","Try to make the password visible by clicking on the eye icon to check your typing",],
# },
# )

# PERSON DATA PROJECT
# POST DATA PROJECT

# Building a custom response
# -------------------------
# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse


# app = FastAPI()

# # HTML response
# # ----------------
# @app.get("/html", response_class=HTMLResponse)
# def get_html():
#     return """
# <html>
# <head>
# <title> FAST API </title>
# </head>
# <body>
# <h1> Basics of FastAPI </h1>
# </body>
# </html>
# # """


# # Plain Text response
# # ----------------------
# @app.get("/text", response_class=PlainTextResponse)
# def text():
#     return "Hello Meghana!"


# # # Making a redirection
# # -----------------------
# @app.get('/redirect')
# def redirect():
#     return RedirectResponse("/html")

