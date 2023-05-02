"""The entrypoint fot the app"""
from databases import Database
from fastapi import FastAPI, status, Depends, HTTPException
from database.database import database, sqlalchemy_engine, get_database
from models.posts_model import PostCreate, PostDB, metadata

app = FastAPI()


async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)


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


@app.get('/', name="Root endpoint", description="An endpoint to test the app")
async def root() -> dict[str, str]:
    """The root endpoint for the app

    Returns:
        dict[str, str]: A simple message to show that the backend works
    """
    return {'message': 'Hello World'}


@app.post("/posts", name="Create a post", description="Endpoint to create a post", status_code=status.HTTP_201_CREATED, response_model=PostDB)
async def create_post(_post: PostCreate, _database: Database = Depends(get_database)) -> PostDB:
    """A create post enpoint

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
