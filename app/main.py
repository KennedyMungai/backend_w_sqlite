"""The entrypoint fot the app"""
from typing import Tuple, List

from databases import Database
from fastapi import Depends, FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from database.database import database, sqlalchemy_engine
from models.posts_model import (PostBase, PostCreate, PostDB,
                                PostPartialUpdate, metadata)

app = FastAPI()

motor_client = AsyncIOMotorClient("mongodb://localhost:27017")

# Connecting to the whole server
database = motor_client["dumb_blogs"]


def get_database() -> AsyncIOMotorDatabase:
    return database


async def get_post_or_404(
    id: ObjectId = Depends(get_object_id), database: AsyncIOMotorDatabase = Depends(get_database)
) -> PostDB:
    raw_post = await database['dumb_blogs'].find_one({"_id": id})


async def pagination(skip: int = 0, limit: int = 10) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


@app.on_event('startup')
async def startup():
    """Database connection code runs on startup
    """
    await database.connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event('shutdown')
async def shutdown():
    """Database disconnection code runs on shutdown

    """
    await database.disconnect()


@app.get(
    '/',
    name="Root endpoint",
    description="An endpoint to test the app",
    tags=['Root']
)
async def root() -> dict[str, str]:
    """The root endpoint for the app

    Returns:
        dict[str, str]: A simple message to show that the backend works
    """
    return {'message': 'Hello World'}


@app.post(
    "/posts",
    name="Create a post",
    description="Endpoint to create a post",
    status_code=status.HTTP_201_CREATED,
    response_model=PostDB,
    tags=['Posts']
)
async def create_post(
    _post: PostCreate,
    _database: Database = Depends(get_database)
) -> PostDB:
    """A create post endpoint

    Args:
        post (PostCreate): The schema for the post to be created
        database (Database, optional): The database connection. Defaults to Depends(get_database).

    Returns:
        PostDB: The template for the returned data
    """
    _post_db = PostDB(**_post.dict())
    await _database['dumb_blogs'].insert_one(_post_db.dict(by_alias=True))

    _post_db = await get_post_or_404(_post_db.id, _database)

    return _post_db


@app.get("/posts")
async def list_posts(
    pagination: Tuple[int, int] = Depends(pagination),
    database: AsyncIOMotorDatabase = Depends(get_database)
) -> List[PostDB]:
    """A list posts endpoint

    Args:
        pagination (Tuple[int, int], optional): The pagination parameters. Defaults to (0, 10).

    Returns:
        List[PostDB]: A list of posts
    """
    skip, limit = pagination
    query = database["dumb_blog"].find({}, skip=skip, limit=limit)

    results = [PostDB(**raw_post) async for raw_post in query]

    return results


@app.get(
    "/posts/{_id}",
    name='Get Single Post',
    description="Returns a single post of the given Id",
    response_model=PostDB,
    tags=["Post"]
)
async def get_post(_post: PostDB = Depends(get_post_or_404)) -> PostDB:
    """A get single post endpoint

    Args:
        post (PostDB, optional): The post to be returned. Defaults to Depends(get_database).

    Returns:
        PostDB: The post to be returned
    """
    return _post
