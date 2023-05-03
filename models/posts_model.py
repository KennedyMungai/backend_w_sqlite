"""The file containing the model for the posts data"""
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

from pydantic import BaseModel, Field
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, MetaData,
                        String, Table, Text)


class PostBase(BaseModel):
    """The base model for the posts data

    Args:
        BaseModel (Pydantic): The parent of all pydantic models
    """
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        """The config subclass for the PostBase model"""
        orm_mode = True


class PostPartialUpdate(BaseModel):
    """The partial update model class

    Args:
        BaseModel (Pydantic): The parent of all pydantic models
    """
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    """The PostCreate base model

    Args:
        PostBase (PostBase): The base Model for thr posts data
    """
    pass


class PostDB(PostBase):
    """The version of the data that is stored in the database

    Args:
        PostBase (PostBase class): The base model for the posts data
    """
    id: int


# class PostPublic(PostDB):
#     comments: List[CommentDB]

class PyObjectId(ObjectId):
    """The ObjectId class for the Pydantic model"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoBaseModel(BaseModel):
    """The base model for the mongo data

    Args:
        BaseModel (Pydantic): The parent of all pydantic models
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


metadata = MetaData()


posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('publication_date', DateTime(), nullable=False),
    Column('title', String(255), nullable=False),
    Column('content', Text, nullable=False),
)

comments = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
    Column("publication_date", DateTime, nullable=False),
    Column("content", Text, nullable=False)
)
