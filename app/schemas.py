from enum import Enum
from typing import Union, List

from pydantic import BaseModel


# Generic Response
class ResponseT(BaseModel):
    code: int
    message: str = "Success"
    data: Union[list, dict] = None


# Notice
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


# ClassRoom
class ClassRoom(BaseModel):
    class MiniIndex(BaseModel):
        # a, b, c, d, e 代表每一天的大节课数：
        # 0 -> 没课，1 -> 有课
        a: int = 0
        b: int = 0
        c: int = 0
        d: int = 0
        e: int = 0

    address: str = None
    num: int = -1
    type: str = None
    data: List[MiniIndex] = []
    # week: int = -1
    # updatedAt = models.DateTimeField(auto_now=True)


# User
class User(BaseModel):
    username: int
    password: str

    class Config:
        orm_mode = True


# UserInfo
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
    enrollDate: str = None
    graduateDate: str = None
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


# CourseTable
class CourseTableSchedule(BaseModel):
    room: str = None
    weekday: int = None
    index: int = None
    weeksString: str = None
    weeks: Union[list, None] = []


class CourseTable(BaseModel):
    code: str
    name: str = None
    teacher: str = None
    credit: str = None
    schedules: List[CourseTableSchedule] = []

    def self_dict(self):
        return self.dict()


# GradeTable
class GradeTable(BaseModel):
    class CourseStatusEnum(str, Enum):
        normal = "正常"
        makeUp = "补考"
        reStudy = "重修"

    name: str
    credit: str = None
    semester: str = None
    status: CourseStatusEnum = CourseStatusEnum.normal
    result: str = None


# Grade
class Grade(GradeTable):
    code: str
    courseType: str = None
    usual: str = None
    midTerm: str = None
    endTerm: str = None
    makeUpScore: str = None
    makeUpScoreResult: str = None
    point: str = None


# GPA
class GPA(BaseModel):
    semester: str = "all"
    gradePointAverage: float = 0.0
    weightedAverage: float = 0.0
    gradePointTotal: float = 0.0
    scoreTotal: float = 0.0
    creditTotal: float = 0.0
    courseCount: int = 0


class AiPaoUser(BaseModel):
    id: int
    code: str
    token: str = ''
    name: str = ''
    gender: str = ''
    schoolName: str = ''
    successCount: int = -1
    failureCount: int = -1
    isCodeValid: bool = False
    isDoneToday: bool = False


class QualityActivity(BaseModel):
    type: str
    id: int
    name: str = ''
    semester: str = ''
    activityDate: str = ''
    location: str = ''
    responsibility: str = ''
    loggingDateTime: str = ''
    status: str = ''
    comment: Union[str, None] = None


class QualityScholarship(BaseModel):
    id: int
    semester: str = ''
    activityType: str = ''
    activityContent: str = ''
    activityLevel: str = ''
    creditType: str = ''
    credit: str = ''
