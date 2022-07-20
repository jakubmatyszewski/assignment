from fastapi import HTTPException


ForbiddenException = HTTPException(
    status_code=401,
    detail="Always look on the bright side of life"
)

