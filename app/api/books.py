
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.db import schemas
from app.db.database import get_db, Books
from app.db.schemas import UserInDB
from app.utils.decorators import unrestricted_users
from app.utils.login import login_manager

router = APIRouter()


@router.get("/books", response_model=List[schemas.Book])
def get_books(db: Session = Depends(get_db)) -> List[schemas.Book]:
    books = Books.get_all_books(db)
    return books


@router.get("/books/{author}/{title}", response_model=schemas.Book)
def get_book(author: str, title: str, db: Session = Depends(get_db)) -> schemas.Book:
    book = Books.get_a_book(author, title, db)
    return book

@unrestricted_users
@router.post("/books", response_model=schemas.Book)
def publish_a_book(
    book: schemas.Book,
    db: Session = Depends(get_db),
    _user: UserInDB = Depends(login_manager),
) -> schemas.Book:

    if book.author == _user.pseudonym:
        book = Books.add_a_book(book, db)
        return book
    else:
        raise HTTPException(status_code=401, detail="User not authorized to perfom action.")

@router.put("/books", response_model=schemas.Book)
def update_a_book(
    book: schemas.Book,
    db: Session = Depends(get_db),
    _user: UserInDB = Depends(login_manager),
) -> schemas.Book:

    if book.author == _user.pseudonym:
        book = Books.update_a_book(book, db)
        return book
    else:
        raise HTTPException(status_code=401, detail="User not authorized to perfom action.")


@router.delete("/books/{author}/{title}")
def delete_a_book(
    author: str,
    title: str,
    db: Session = Depends(get_db),
    _user: UserInDB = Depends(login_manager),
) -> dict:

    if author == _user.pseudonym:
        status = Books.delete_a_book(author, title, db)
        if status:
            return {"msg": f"Successfully deleted book {title} by {author}"}
        else:
            return {"msg": f"Failed to delete book {title} by {author}"}
    else:
        raise HTTPException(status_code=401, detail="User not authorized to perfom action.")
