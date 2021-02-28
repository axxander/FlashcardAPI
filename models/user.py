from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    firstname = fields.CharField(max_length=30)
    surname = fields.CharField(max_length=30)
    email = fields.CharField(
        max_length=254,
        unique=True
    )
    username = fields.CharField(
        max_length=60, 
        unique=True
    )
    hashed_password = fields.CharField(max_length=140)  # not sure on hash length?