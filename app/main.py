"""The entrypoint fot the app"""
from fastapi import FastAPI
from database.database import database, sqlalchemy_engine
from models.posts_model import metadata

app = FastAPI()


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
