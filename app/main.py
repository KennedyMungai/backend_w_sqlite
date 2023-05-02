"""The entrypoint fot the app"""
from fastapi import FastAPI

app = FastAPI()


@app.get('/', name="Root endpoint", description="An endpoint to test the app")
async def root() -> dict[str, str]:
    """The root endpoint for the app

    Returns:
        dict[str, str]: A simple message to show that the backend works
    """
    return {'message': 'Hello World'}
