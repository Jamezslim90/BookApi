from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel




app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}




# from typing import Union
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# @app.get("/")
# def read_root():
#     return {"Hello": "James"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}



# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


# Dog API Example

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional
# from uuid import uuid4, UUID

# app = FastAPI()

# class Book(BaseModel):
#     id: Optional[UUID] = uuid4()
#     title: str
#     author: str
#     description: Optional[str] = None

# # In-memory storage
# books_db: List[Book] = []

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# @app.get("/books/", response_model=List[Book])
# async def get_all_books():
#     return books_db

# @app.post("/books/", response_model=Book)
# async def create_book(book: Book):
#     books_db.append(book)
#     return book

# @app.get("/books/{book_id}", response_model=Book)
# async def get_a_book(book_id: UUID):
#     for book in books_db:
#         if book.id == book_id:
#             return book
#     raise HTTPException(status_code=404, detail="Book not found")

# @app.put("/books/{book_id}", response_model=Book)
# async def update_book(book_id: UUID, updated_book: Book):
#     for index, book in enumerate(books_db):
#         if book.id == book_id:
#             books_db[index] = updated_book
#             return updated_book
#     raise HTTPException(status_code=404, detail="Book not found")

# @app.delete("/books/{book_id}")
# async def delete_book(book_id: UUID):
#     for index, book in enumerate(books_db):
#         if book.id == book_id:
#             del books_db[index]
#             return {"detail": "Book deleted"}
#     raise HTTPException(status_code=404, detail="Book not found")


