from fastapi import FastAPI, Depends, Request
from app.database import engine, get_db
from app.models.base import Base
from app.models.user import User
from app.routers.auth import router
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def home(
    request: Request,
    user: Session= Depends(get_current_user),
    db:Session = Depends(get_db)):
    return {'Message':f"Successfully getting the data {user.password}"}

