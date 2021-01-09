from fastapi import APIRouter
from fastapi_sqlalchemy import db

from app import schemas
from appDB import crud

router = APIRouter()


@router.post("/notification-register", response_model=schemas.ResponseT, summary='绑定 Notification Token')
async def register_notification(form: schemas.NotificationToken):
    """
        绑定 Notification Token
    - **token**: 来自 Apple Push Notification Service 的 deviceToken
    - **username**: 在本系统登录过的教务在线学号
    """
    response = schemas.ResponseT(data=form)
    response.code, response.message = crud.register_notification(form, session=db.session)
    return response


@router.post("/notification-remove", response_model=schemas.ResponseT, summary='取消绑定 Notification Token')
async def remove_notification(form: schemas.NotificationToken):
    """
        取消绑定 Notification Token
    - **token**: 来自 Apple Push Notification Service 的 deviceToken
    - **username**: 在本系统登录过的教务在线学号
    """
    response = schemas.ResponseT(data=form)
    response.code, response.message = crud.remove_notification(form, session=db.session)
    return response
