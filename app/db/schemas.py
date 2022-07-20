from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    pseudonym: str
    password: str
    enabled: bool

class UserInDB(BaseModel):
    username: str
    pseudonym: str
    hashed_password: str
    enabled: bool

    class Config:
        orm_mode = True

class Book(BaseModel):
    id: int = None
    title: str
    description: str
    author: str
    cover: str
    price: int

    class Config:
        orm_mode = True

class UserExtended(UserInDB):
    books: List[Book]
