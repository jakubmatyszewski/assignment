from app.db.database import get_user_by_username, get_db
from app.utils.login import login_manager, verify_password

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session


router = APIRouter()

@router.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = data.username

    user = get_user_by_username(username, db)
    if not user:
        raise InvalidCredentialsException
    elif not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    access_token = login_manager.create_access_token(
        data={'sub': username}
    )
    return {'access_token': access_token}
