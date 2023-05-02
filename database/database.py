"""The database connection logic"""

from databases import Database
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///./data.db"
database = Database(DATABASE_URL)

sqlalchemy_engine = create_engine(DATABASE_URL)


def get_database() -> Database:
    """A function that calls the database connection

    Returns:
        Database: The database connection

    """
    return database
