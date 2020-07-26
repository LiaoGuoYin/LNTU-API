from typing import Union

from pydantic import BaseModel

from app.exceptions import StatusCodeEnum


class ResponseT(BaseModel):
    code: StatusCodeEnum = StatusCodeEnum.SUCCESS
    message: str = "success"
    data: Union[list, dict] = []


class User(BaseModel):
    username: int
    password: str
