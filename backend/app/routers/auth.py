from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token, 
)
from app.schemas.user_pydantic import UserModel
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(data: UserModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists. Please login or use forgot password."
        )

    new_user = User(
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "email": new_user.email,
        "message": "User registered successfully. Please login."
    }


@router.post("/login")
def login(
    user: UserModel,
    response: Response,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="User not registered. Please register."
        )


    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )


    access_token = create_access_token({"sub": existing_user.email})
    refresh_token = create_refresh_token({"sub": existing_user.email})


    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return {
        "message": "Successfully logged in",
        "user_email": existing_user.email,
        "user_authenticated": True
    }


@router.post("/logout")
def logout(
    response: Response,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax"
    )

    return {"message": "Successfully logged out"}
