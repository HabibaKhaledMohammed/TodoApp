# from fastapi import FastAPI, HTTPException, Path, Query
# from pydantic import BaseModel, Field
# from starlette import status
#
# app = FastAPI()
#
#
# class Book(BaseModel):
#     id: int
#     title: str
#     author: str
#     category: str
#     description: str
#     rating: float
#
#
# class BookCreate(BaseModel):
#     title: str = Field(min_length=3, description="Book title")
#     author: str = Field(min_length=3, description="Book author")
#     category: str = Field(min_length=3, description="Book category")
#     description: str = Field(min_length=3, description="Book description")
#     rating: float = Field(gt=0, lt=5, description="Book rating")
#
#
# class BookUpdate(BaseModel):
#     title: str | None = None
#     author: str | None = None
#     category: str | None = None
#     description: str | None = None
#     rating: float | None = None
#
#
# BOOKS: list[Book] = [
#     Book(
#         id=1,
#         title="Atomic Habits",
#         author="James Clear",
#         category="Self-Help",
#         description="A practical guide to building good habits and breaking bad ones.",
#         rating=4.8,
#     ),
#     Book(
#         id=2,
#         title="The Alchemist",
#         author="Paulo Coelho",
#         category="Fiction",
#         description="A philosophical novel about following your personal legend.",
#         rating=4.5,
#     ),
#     Book(
#         id=3,
#         title="Clean Code",
#         author="Robert C. Martin",
#         category="Programming",
#         description="Guidance on writing readable, maintainable, and robust code.",
#         rating=4.7,
#     ),
#     Book(
#         id=4,
#         title="Deep Work",
#         author="Cal Newport",
#         category="Productivity",
#         description="Strategies for focused work in a distracted world.",
#         rating=4.6,
#     ),
# ]
#
#
# @app.get("/api-endpoint", status_code=status.HTTP_200_OK)
# def hello_api(name: str | None = None):
#     return {"message": "Hello Habiba Khaled!"}
#
#
# @app.get("/books")
# def list_books():
#     return {"books": BOOKS}
#
#
# @app.get("/books/by-rating")
# def get_books_by_rating(rating: float = Query(gt=0, lt=5)):
#     matching_books = [book for book in BOOKS if book.rating == rating]
#     return {"books": matching_books}
#
#
# @app.get("/books/{title}")
# def get_book_by_title(title: str):
#     for book in BOOKS:
#         if book.title.lower() == title.lower():
#             return {"book": book}
#
#     raise HTTPException(status_code=404, detail="Book not found")
#
#
# @app.post("/books/create_book")
# def add_book(book: BookCreate):
#     new_book = Book(
#         id=max(existing_book.id for existing_book in BOOKS) + 1 if BOOKS else 1,
#         title=book.title,
#         author=book.author,
#         category=book.category,
#         description=book.description,
#         rating=book.rating,
#     )
#     BOOKS.append(new_book)
#     return {"message": "Book added successfully", "book": new_book}
#
#
# @app.put("/books/{book_id}")
# def replace_book(book: BookCreate,book_id: int = Path(gt=0)):
#     for index, existing_book in enumerate(BOOKS):
#         if existing_book.id == book_id:
#             updated_book = Book(
#                 id=book_id,
#                 title=book.title,
#                 author=book.author,
#                 category=book.category,
#                 description=book.description,
#                 rating=book.rating,
#             )
#             BOOKS[index] = updated_book
#             return {"message": "Book updated successfully", "book": updated_book}
#
#     raise HTTPException(status_code=404, detail="Book not found")
#
#
# @app.patch("/books/{book_id}")
# def update_book(book_id: int, book: BookUpdate):
#     for index, existing_book in enumerate(BOOKS):
#         if existing_book.id == book_id:
#             updated_book = existing_book.model_copy(
#                 update=book.model_dump(exclude_unset=True)
#             )
#             BOOKS[index] = updated_book
#             return {"message": "Book updated successfully", "book": updated_book}
#
#     raise HTTPException(status_code=404, detail="Book not found")
#
#
# @app.delete("/books/{book_id}")
# def delete_book(book_id: int):
#     for index, book in enumerate(BOOKS):
#         if book.id == book_id:
#             deleted_book = BOOKS.pop(index)
#             return {"message": "Book deleted successfully", "book": deleted_book}
#
#     raise HTTPException(status_code=404, detail="Book not found")
#
#
# if __name__ == "__main__":
#     hello_api("PyCharm")
