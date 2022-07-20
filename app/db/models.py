from app.db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint


class UserORM(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, unique=True, index=True)
    pseudonym = Column(String, unique=True,)
    hashed_password = Column(String)
    enabled = Column(Boolean, default=True)

class BookORM(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author = Column(String, ForeignKey("users.pseudonym"))
    cover = Column(String)
    price = Column(Integer)

    __table_args__ = (
        UniqueConstraint('author', 'title'),
      )
