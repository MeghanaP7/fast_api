from fastapi import FastAPI, Depends, status, HTTPException
from database import database, sqlalchemy_engine, get_database
from models import metadata, posts
from pydantic import BaseModel, Field
from databases import Database
from datetime import datetime
from typing import Tuple, List, Optional, cast, Mapping

app = FastAPI()


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime


class PostCreate(PostBase):
    id: int
    pass


class PostPublic(PostBase):
    id: int


class PostDB(PostBase):
    id: int
    nb_views: int = 0


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# class CommentBase(BaseModel):
#     post_id: int
#     commented_date: datetime = Field(default_factory=datetime.now)
#     comment: str
#
#
# class CommentCreate(CommentBase):
#     pass
#
#
# class CommentDB(CommentBase):
#     id: int
#
#
# class PostPublic(PostDB):
#     comments: List[CommentDB]


@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def pagination(skip: int = 0, limit: int = 10) -> Tuple[int, int]:
    return (skip, limit)


async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_query)
    print(raw_post)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, database: Database = Depends(get_database)
) -> PostDB:
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)
    print(post_id)
    post_db = await get_post_or_404(post_id, database)
    return post_db


@app.get("/posts")
async def list_posts(
    pagination: Tuple[int, int] = Depends(pagination),
    database: Database = Depends(get_database),
) -> List[PostDB]:
    skip, limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)
    results = [PostDB(**row) for row in rows]
    return results


@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostDB = Depends(get_post_or_404),
    database: Database = Depends(get_database),
) -> PostDB:
    update_query = (
        posts.update()
        .where(posts.c.id == post.id)
        .values(post_update.dict(exclude_unset=True))
    )
    await database.execute(update_query)
    post_db = await get_post_or_404(post.id, database)
    return post_db


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostDB = Depends(get_post_or_404), database: Database = Depends(get_database)
):
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_individual_post(
    id: int,
    database: Database = Depends(get_database)
):
    select_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_query)
    print(raw_post)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)


# @app.post("/comments", response_model=CommentDB, status_code=status.HTTP_201_CREATED)
# async def create_comment(
#     comment: CommentCreate, database: Database = Depends(get_database)
# ) -> CommentDB:
#     select_post_query = posts.select().where(posts.c.id == comment.post_id)
#     post = await database.fetch_one(select_post_query)
#     if post is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post {id} does not exist"
#         )
#     insert_query = comments.insert().values(comment.dict())
#     comment_id = await database.execute(insert_query)
#     select_query = comments.select().where(comments.c.id == comment_id)
#     raw_comment = cast(Mapping, await database.fetch_one(select_query))
#     return CommentDB(**raw_comment)
#

# Setting up a database migration system with Alembic

# pip install alembic


# alembic init alembic


# alembic revision --autogenerate -m "Initial migration"


# alembic upgrade head
