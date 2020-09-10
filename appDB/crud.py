import datetime

from sqlalchemy.orm import Session

from app import schemas
from appDB import models


def update_user(user: schemas.User, session: Session) -> models.User:
    new_user = models.User(**user.dict())
    new_user.lastLogin = datetime.datetime.now()
    session.merge(new_user)
    session.commit()
    return new_user


def update_info(user_info: schemas.UserInfo, session: Session) -> models.UserInfo:
    new_user_info = models.UserInfo(**user_info.dict())
    new_user_info.ownerUsername = user_info.username
    session.merge(new_user_info)
    session.commit()
    return new_user_info
