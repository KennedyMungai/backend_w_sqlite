"""The database connection logic"""

from databases import Database
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///./data.db"
database = Database(DATABASE_URL)

sqlalchemy_engine = create_engine(DATABASE_URL)
