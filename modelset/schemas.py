from typing import List, Optional, TypeVar, Generic, Set

from pydantic import BaseModel
from pydantic.generics import GenericModel
from starlette import status

# Common
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


# Notice
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


class NoticeDetailAppendix(BaseModel):
    url: str
    name: str


class NoticeDetail(BaseModel):
    title: str = None
    date: str = None
    content: str = None
    appendix: List[NoticeDetailAppendix] = []


class Notice(BaseModel):
    url: str
    detail: Set[NoticeDetail] = NoticeDetail()


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


# Score
ScoreTemplate = {
    "code": "H271780001036.18",
    "name": "高等数学1",
    "grade": '99',
    "semester": "2017-2018 1",
    "courseType": "必修",
    "credit": '2.0',
    "gradeDetail": {
        "ususl": "100",
        "interim": "40",
        "final": "23",
        "general": "99",
    }
}


class GradeDetail(BaseModel):
    usual: str = None
    interim: str = None
    final: str = None
    general: str = None


class Grade(BaseModel):
    code: str
    semester: str = None
    name: str = None
    courseType: str = None
    grade: str = None
    credit: str = None
    gradeDetail: Set[GradeDetail] = {}
