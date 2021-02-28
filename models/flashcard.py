from tortoise import fields
from tortoise.models import Model

from .user import User


class Flashcard(Model):
    id = fields.IntField(pk=True)
    category = fields.CharField(max_length=140)
    question = fields.CharField(max_length=280)
    answer = fields.CharField(max_length=280)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        to_field="id"
    )