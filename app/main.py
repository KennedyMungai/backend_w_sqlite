"""The entrypoint fot the app"""
from typing import Tuple

from databases import Database
from fastapi import Depends, FastAPI, HTTPException, status

from database.database import database, get_database, sqlalchemy_engine
from models.posts_model import PostBase, PostCreate, PostDB, metadata

app = FastAPI()


async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)


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


@app.get('/', name="Root endpoint", description="An endpoint to test the app", tags=['Root'])
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
async def create_post(_post: PostCreate, _database: Database = Depends(get_database)) -> PostDB:
    """A create post endpoint

    Args:
        post (PostCreate): The schema for the post to be created
        database (Database, optional): The database connection. Defaults to Depends(get_database).

    Returns:
        PostDB: The template for the returned data
    """
    insert_query = posts.insert().values(_post.dict())
    post_id = await _database.execute(insert_query)
    post_db = await get_post_or_404(post_id, _database)

    return post_db


@app.get(
    "/posts",
    name="Get all posts",
    description="Endpoint to get all posts",
    response_model=list[PostDB],
    tags=['Posts']
)
async def list_posts(
    _pagination: Tuple[int, int] = Depends(pagination),
    _database: Database = Depends(get_database)
) -> list[PostDB]:
    """List all posts from the database

    Args:
        _pagination (Tuple[int, int], optional): This defined pagination for the data fetched. Defaults to Depends(pagination).
        _database (Database, optional): The database connection. Defaults to Depends(get_database).

    Returns:
        list[PostDB]: A list of all the posts from the database
    """
    skip, limit = _pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await _database.fetch_all(select_query)

    results = [PostDB(**row) for row in rows]

    return results


@app.get("/posts/{id}", name="Get a post", description="Endpoint to get a post", response_model=PostDB, tags=['Posts'])
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    """Get a post from the database

    Args:
        post (PostDB, optional): The post to be fetched. Defaults to Depends(get_post_or_404).

    Returns:
        PostDB: The post fetched from the database
    """
    return post
