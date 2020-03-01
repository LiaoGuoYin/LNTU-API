from pydantic import BaseModel


class User(BaseModel):
    username: int
    password: str
