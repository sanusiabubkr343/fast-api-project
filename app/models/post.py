from tortoise import models, fields


class Post(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.User", related_name="posts")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    comments = fields.ReverseRelation["Comment"]
    votes = fields.ReverseRelation["Vote"]


class Comment(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    post = fields.ForeignKeyField("models.Post", related_name="comments")
    author = fields.ForeignKeyField("models.User", related_name="comments")
    created_at = fields.DatetimeField(auto_now_add=True)


class Vote(models.Model):
    id = fields.IntField(pk=True)
    post = fields.ForeignKeyField("models.Post", related_name="votes")
    user = fields.ForeignKeyField("models.User", related_name="votes")
