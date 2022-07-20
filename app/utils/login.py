from datetime import timedelta
from fastapi_login import LoginManager
from app.main import SETTINGS

SECRET = SETTINGS.SECRET_KEY
login_manager = LoginManager(SECRET, "/login", default_expiry=timedelta(hours=12))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return login_manager.pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return login_manager.pwd_context.hash(password)
