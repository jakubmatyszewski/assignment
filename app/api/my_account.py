from fastapi import APIRouter, Depends
from app.db import schemas
from app.db.database import get_user_details, get_db
from app.utils.login import login_manager
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/me", response_model=schemas.UserExtended)
def my_account(
    _db: Session = Depends(get_db), _user: schemas.UserInDB = Depends(login_manager)
):
    user_details = get_user_details(_user.username, _db)
    return user_details
