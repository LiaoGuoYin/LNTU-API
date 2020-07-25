from typing import Union

from pydantic import BaseModel


class ResponseT(BaseModel):
    code: int = 200
    message: str = "success"
    data: Union[list, dict] = []


class User(BaseModel):
    username: int
    password: str
