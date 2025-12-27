from fastapi import Request, HTTPException, Depends 
from sqlalchemy.orm import Session 
from app.models.base import Base
from app.models.user import User 
from app.core.security import decode_access_token
from app.database import get_db


def get_current_user(request: Request,db:Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code = 401, detail = "Not Authenticated")

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code = 401, detail = "Invalid Token")

    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code = 401, details = "User Not Found")
    return user
