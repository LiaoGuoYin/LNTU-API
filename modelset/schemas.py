from typing import List, Optional, TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel
from starlette import status

# Common
DataT = TypeVar('DataT')


class Response(BaseModel):
    code: int = status.HTTP_200_OK
    message: str = "success"
    data: Optional[DataT]


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


# Notice
noticeTemplate = {
    'url': '',
    'title': '',
    'date': '',
    'content': '',
    'appendix': [{
        'url': '',
        'name': '',
    }],
}


class NoticeDetail(BaseModel):
    class NoticeDetailAppendix(BaseModel):
        url: str
        name: str

    title: str = None
    date: str = None
    content: str = None
    appendix: List[NoticeDetailAppendix] = []


class Notice(NoticeDetail):
    url: str


## ClassTable
classTableTemplate = {
    "name": "会计学",
    "credit": "2.5",
    "code": "H101730004040.01",
    "teacher": "冯旭日",
    "schedule": [{
        "code": "H101730004040.01",
        "room": "静远楼238(辽宁工大葫芦岛校区)",
        "weeks": "单1-13",
        "weekday": "5",
        "index": "3"
    }]
}


class ClassTableSchedule(BaseModel):
    code: str
    room: str = None
    weeks: str = None
    weekday: str = None
    index: str = None


class ClassTable(BaseModel):
    code: str
    name: str = None
    teacher: str = None
    credit: str = None
    schedule: List[ClassTableSchedule] = []


## GPA
gpa_dict = {
    'GPA': '',
    'counts': '',
    'credits': '',
    'GPAs': [{
        'yearSection': '',
        'semester': '',
        'count': '',
        'credit': '',
        'semesterGPA': '',
    }],
    'time': ''
}


class semesterGPA(BaseModel):
    yearSection: str
    semester: str = None
    count: str = None
    credit: str = None
    semesterGPA: str = None


class GPA(BaseModel):
    GPA: str
    counts: str = None
    credits: str = None
    effectiveTime: str = None
    GPAs: List[semesterGPA] = []


# Grade
GradeTemplate = {
    "code": "H271780001036.18",
    "name": "高等数学1",
    "semester": "2017-2018 1",
    "courseType": "必修",
    "credit": "2.0",
    "usual": "100",
    "midterm": "40",
    "termEnd": "23",
    "result": "99"
}


class Grade(BaseModel):
    code: str = ''
    name: str = ''
    semester: str = ''
    courseType: str = ''
    grade: str = ''
    credit: str = ''
    usual: str = ''
    midterm: str = ''
    termEnd: str = ''
    result: str = ''

    class Config:
        orm_mode = True


class User(BaseModel):
    username: int
    password: str

    # grades: List[Grade] = []

    class Config:
        orm_mode = True
