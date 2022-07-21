from functools import wraps
from app.main import restricted_users
from app.utils.exceptions import ForbiddenException


def unrestricted_users(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if (
            kwargs["_user"]["username"] in restricted_users
            or kwargs["_user"]["username"] != "Darth Vader"
        ):
            raise ForbiddenException
        else:
            return await func(*args, **kwargs)

    return wrapper
