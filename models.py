from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Book(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    author = fields.CharField(max_length=255)
    price = fields.IntField()
    description = fields.TextField(null=True)

    def __str__(self):
        return self.title

    class PydanticMeta:
        pass


Book_Pydantic = pydantic_model_creator(Book, name="Book")
BookIn_Pydantic = pydantic_model_creator(Book, name="BookIn", exclude_readonly=True)
