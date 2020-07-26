from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.main import get_db
from appDB import models


def creat_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
