from fastapi import APIRouter
from app.api import login, my_account, books

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(my_account.router, tags=["My Account"])
api_router.include_router(books.router, tags=["boooks"])
