from fastapi import HTTPException
from typing import List, Union
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


from app.main import SETTINGS
from app.db import Base, schemas, models
from app.utils import login

DATABASE_URL = f"postgresql://{SETTINGS.DB_USER}:{SETTINGS.DB_PASSWORD}@{SETTINGS.DB_ADDRESS}/{SETTINGS.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(user: schemas.User, db: Session) -> bool:
    """
    Create new user

    return: True if user was created successfully
    return: False if user already exists in database
    """
    hashed_password = login.get_password_hash(user.password)
    if not get_user_by_username(user.username, db):
        user = models.UserORM(
            username=user.username,
            pseudonym=user.pseudonym,
            hashed_password=hashed_password,
            enabled=user.enabled,
        )
        # Add user to db
        db.add(user)
        db.commit()
        return True
    else:
        return False


@login.login_manager.user_loader()
def get_user_by_username(username: str, db: Session = None) -> schemas.UserInDB:
    """
    Returns user data with given username
    """

    if not db:
        db = next(get_db())

    return db.query(models.UserORM).filter(models.UserORM.username == username).first()


def init_empty_user_db(db: Session) -> None:
    """
    Init user if database was empty.
    """

    user_data = schemas.User(
        **{
            "username": "admin",
            "pseudonym": "TheAdmin",
            "password": "adm1n",
            "enabled": True,
        }
    )

    create_user(user_data, db)


def verify_new_user(user_data: schemas.User, db: Session) -> Union[dict, None]:
    username_used = (
        db.query(models.UserORM).filter(models.UserORM.username == user_data.username).first()
    )
    if username_used:
        return {"msg": "Username already in use."}

    pseudonym_used = (
        db.query(models.UserORM).filter(models.UserORM.pseudonym == user_data.pseudonym).first()
    )
    if pseudonym_used:
        return {"msg": "Pseudonym already in use."}

    if len(user_data.password) < 6:
        return {"msg": "Please use password that is at least 6 characters long."}


def get_user_details(username: str, db: Session) -> schemas.UserExtended:
    user = db.query(models.UserORM).filter(models.UserORM.username == username).first()
    books = (
        db.query(models.BookORM).filter(models.BookORM.author == user.pseudonym).all()
    )

    tmp = user.__dict__
    tmp["books"] = books

    return schemas.UserExtended(**tmp)


class Books:
    def __init__(self):
        pass

    def get_all_books(db: Session) -> List[models.BookORM]:
        return db.query(models.BookORM).all()

    def get_a_book(author: str, title: str, db: Session) -> models.BookORM:
        book = (
            db.query(models.BookORM)
            .filter(models.BookORM.author == author)
            .filter(models.BookORM.title == title)
            .first()
        )
        return book

    def add_a_book(book: schemas.Book, db: Session) -> models.BookORM:
        db_book = models.BookORM(
            title=book.title,
            description=book.description,
            author=book.author,
            cover=book.cover,
            price=book.price,
        )
        db.add(db_book)
        try:
            db.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="This author already published a book with this title.",
            )
        else:
            return db_book

    def update_a_book(book: schemas.Book, db: Session) -> models.BookORM:
        db_book = (
            db.query(models.BookORM)
            .filter(models.BookORM.author == book.author)
            .filter(models.BookORM.title == book.title)
            .first()
        )

        for key, new_value in book:
            if key != "id":
                setattr(db_book, key, new_value)

        try:
            db.commit()
        except Exception as e:
            print(e)
        finally:
            return db_book

    def delete_a_book(author: str, title: str, db: Session) -> bool:
        book = (
            db.query(models.BookORM)
            .filter(models.BookORM.author == author)
            .filter(models.BookORM.title == title)
            .first()
        )
        db.delete(book)
        try:
            db.commit()
        except Exception as e:
            print(e)
            return False
        else:
            return True
