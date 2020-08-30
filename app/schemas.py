import datetime
from typing import Union, List

from pydantic import BaseModel

from app.exceptions import StatusCodeEnum


class ResponseT(BaseModel):
    code: StatusCodeEnum = StatusCodeEnum.SUCCESS
    message: str = "success"
    data: Union[list, dict] = []


class User(BaseModel):
    username: int
    password: str

    class Config:
        orm_mode = True


class Grade(BaseModel):
    code: str = None
    name: str = None
    semester: str = None
    courseType: str = None
    grade: str = None
    credit: str = None
    usual: str = None
    midterm: str = None
    termEnd: str = None
    result: str = None


class ClassTableCourseSchedule(BaseModel):
    room: str = None
    weeks: Union[list, None] = []
    weekday: int = None
    index: int = None


class ClassTableCourse(BaseModel):
    code: str
    name: str = None
    teacher: str = None
    credit: str = None
    schedules: List[ClassTableCourseSchedule] = []

    def self_dict(self):
        return self.dict()


class UserInfo(BaseModel):
    username: int
    name: str
    photoUrl: str = None
    nickname: str = None
    gender: str = None
    grade: str = None
    educationLast: str = None
    project: str = None
    education: str = None
    studentType: str = None
    college: str = None
    major: str = None
    direction: str = None
    enrollDate: datetime.date = None
    graduateDate: datetime.date = None
    chiefCollege: str = None
    studyType: str = None
    membership: str = None
    isInSchool: str = None
    campus: str = None
    majorClass: str = None
    effectAt: str = None
    isInRecord: str = None
    studentStatus: str = None
    isWorking: str = None
