from tortoise import models, fields


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    posts = fields.ReverseRelation["Post"]
    comments = fields.ReverseRelation["Comment"]
    votes = fields.ReverseRelation["Vote"]
