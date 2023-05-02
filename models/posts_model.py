"""The file containing the model for the posts data"""
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Text

metadata = MetaData()


posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('publication_date', DateTime(), nullable=False),
    Column('title', String(255), nullable=False),
    Column('content', Text, nullable=False),
)
