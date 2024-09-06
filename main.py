# Importing FastAPI to create an application instance and HTTPException to handle errors.
# Importing the ORM model `Book` and two Pydantic models:
# `BookIn_Pydantic` for input data, and `Book_Pydantic` for output data.
# Importing Tortoise ORM integration for FastAPI, including a custom 404 error handler and the `register_tortoise` function to connect Tortoise ORM to FastAPI.
# Importing BaseModel from Pydantic, which will be used to define models for request and response validation.
# Importing List from typing to define the type of response as a list of objects.


from fastapi import FastAPI, HTTPException
from models import Book, BookIn_Pydantic, Book_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    message: str
# Defining a simple Pydantic model for response messages (used in the delete operation), with a single field `message`.

app = FastAPI(title="BookAPI", description="A CRUD for Books")
# Creating an instance of the FastAPI app with metadata: title and description.

@app.get('/')
async def read_root():
    return "FastAPi running successfully"
# Defining a basic GET endpoint for the root URL `/`, which returns a success message indicating that the API is running.

@app.get('/books', response_model=List[Book_Pydantic])
async def get_all_books():
    # This endpoint returns all books. The `response_model` is a list of `Book_Pydantic` objects.
    return await Book_Pydantic.from_queryset(Book.all())
    # Fetches all books from the database and converts them into Pydantic models for the response.

@app.post('/book', response_model=Book_Pydantic)
async def create(book: BookIn_Pydantic):
    # This POST endpoint is for creating a new book. The input is a `BookIn_Pydantic` object.
    obj = await Book.create(**book.dict(exclude_unset=True))
    # Creates a new book entry in the database by converting the Pydantic object to a dictionary.
    return await Book_Pydantic.from_tortoise_orm(obj)
    # Converts the newly created database object into a Pydantic model for the response.

@app.get('/book/{id}', response_model=Book_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_one(id: int):
    # This GET endpoint retrieves a book by its ID. If the book is not found, it returns a 404 error.
    return await Book_Pydantic.from_queryset_single(Book.get(id=id))
    # Retrieves a single book from the database and converts it into a Pydantic model.

@app.put("/book/{id}", response_model=Book_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update(id: int, book: BookIn_Pydantic):
    # This PUT endpoint updates a book by its ID. It takes the book data as `BookIn_Pydantic` and updates the database entry.
    await Book.filter(id=id).update(**book.dict(exclude_unset=True))
    # Updates the book entry in the database with the provided fields, skipping unset values.
    return await Book_Pydantic.from_queryset_single(Book.get(id=id))
    # After updating, it fetches the updated book and returns it as a Pydantic model.

@app.delete("/book/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete(id: int):
    # This DELETE endpoint deletes a book by its ID. It returns a success message or a 404 error if the book is not found.
    delete_obj = await Book.filter(id=id).delete()
    # Attempts to delete the book by its ID. If the book is not found, `delete_obj` will be 0.
    if not delete_obj:
        raise HTTPException(status_code=404, detail="This book is not found.")
    # If no book is deleted, raise a 404 error with a message.
    return Message(message="Successfully Deleted")
    # If the book is deleted successfully, return a success message.

register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
# Registers Tortoise ORM with FastAPI, connecting it to a SQLite database.
# It also auto-generates schemas (tables) based on the models and adds exception handlers for database errors.



















































# # Book API Example


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional
# from uuid import uuid4, UUID
# from tortoise.contrib.fastapi import register_tortoise
# from tortoise.models import Model
# from tortoise import fields

# app = FastAPI()

# # Tortoise ORM Model
# class Book(Model):
#     id = fields.UUIDField(pk=True)
#     title = fields.CharField(max_length=255)
#     author = fields.CharField(max_length=255)
#     price = fields.IntField()
#     description = fields.TextField(null=True)

#     class Meta:
#         table = "books"


# class BookSchema(BaseModel):
#     title: str
#     author: str
#     price: int
#     description: Optional[str] = None

#     class Config:
#         orm_mode = True

# # Get all books
# @app.get("/books/", response_model=List[BookSchema])
# async def get_all_books():
#     return await Book.all()

# # Create a book
# @app.post("/books/", response_model=BookSchema)
# async def create_book(book: BookSchema):
#     book_obj = await Book.create(**book.model_dump(exclude_unset=True))
#     return book_obj

# # Get a book by id
# @app.get("/books/{book_id}", response_model=BookSchema)
# async def get_a_book(book_id: UUID):
#     book = await Book.filter(id=book_id).first()
#     if book:
#         return book
#     raise HTTPException(status_code=404, detail="Book not found")

# # Update a book
# @app.put("/books/{book_id}", response_model=BookSchema)
# async def update_book(book_id: UUID, updated_book: BookSchema):
#     book = await Book.filter(id=book_id).first()
#     if book:
#         await book.update_from_dict(updated_book.dict(exclude_unset=True))
#         await book.save()
#         return book
#     raise HTTPException(status_code=404, detail="Book not found")

# # Delete a book
# @app.delete("/books/{book_id}")
# async def delete_book(book_id: UUID):
#     book = await Book.filter(id=book_id).first()
#     if book:
#         await book.delete()
#         return {"detail": "Book deleted"}
#     raise HTTPException(status_code=404, detail="Book not found")



# # async def init():
# #     # Here we create a SQLite DB using file "db.sqlite3"
# #     #  also specify the app name of "models"
# #     #  which contain models from "app.models"
# #     await Tortoise.init(
# #         db_url='sqlite://db.sqlite3',
# #         modules={'models': ['__main__']},
# #     )
# #     # Generate the schema
# #     await Tortoise.generate_schemas()