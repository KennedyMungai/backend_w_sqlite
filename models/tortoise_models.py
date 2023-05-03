"""A file containing tortoise ORM logic"""
from tortoise.fields import IntField, DatetimeField, CharField, TextField
from tortoise.models import Model


class PostTortoise(Model):
    """A class that represents a post in the database

    Args:
        Model (_type_): _description_
    """
    id = IntField(pk=True, generated=True)
    publication_date = DatetimeField(null=False)
    title = CharField(max_length=255, null=False)
    content = TextField(null=False)

    class Meta:
        """The Post Tortoise ORM class"""
        table = "posts"
