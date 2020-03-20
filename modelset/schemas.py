from typing import List, Optional, TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel
from starlette import status

noticeTemplate = {
    'url': '',
    'detail': {
        'title': '',
        'date': '',
        'content': '',
        'appendix': [{
            'url': '',
            'name': '',
        }],
    }
}

DataT = TypeVar('DataT')


class ResponseT(GenericModel, Generic[DataT]):
    code: int = status.HTTP_200_OK
    message: str = "success"
    data: Optional[DataT]

    # @validator('code', always=True)
    # def check_consistency(cls, v, values):
    #     if v is not None and values['data'] is not None:
    #         raise ValueError('must not provide both data and error')
    #     if v is None and values.get('data') is None:
    #         raise ValueError('must provide data or error')
    #     return v


class User(BaseModel):
    username: str
    password: str


class NoticeDetailAppendix(BaseModel):
    url: str
    name: str


class NoticeDetail(BaseModel):
    title: str
    date: str
    content: str
    appendix: List[NoticeDetailAppendix] = []


class Notice(BaseModel):
    url: str
    detail: NoticeDetail = NoticeDetail(**noticeTemplate.get('detail'))
