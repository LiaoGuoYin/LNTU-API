from enum import Enum
from typing import Union, List

from pydantic import BaseModel
from starlette import status


class YamlConfig(BaseModel):
    message: str
    sentryURL: str
    semesterStartDate: str

    host: str
    port: str
    user: str
    password: str
    database: str
    testDatabase: str

    username: str
    educationPassword: str
    qualityPassword: str


# Generic Response
class ResponseT(BaseModel):
    code: int = status.HTTP_200_OK
    message: str = "Success"
    data: Union[list, dict] = None


# Notice


# Classroom
class Classroom(BaseModel):
    room: str = ''
    type: str = ''
    capacity: str = ''
    scheduleList: List[str] = []  # 周一到周天的每天五大节课的列表: '00100' 0 -> 没课，1 -> 有课


class ClassroomResponseData(BaseModel):
    week: str
    buildingName: str
    classroomList: List[Classroom] = []


# User
class User(BaseModel):
    username: str
    password: str


# UserInfo
class UserInfo(BaseModel):
    username: str
    name: str
    photoURL: str = None
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
    scheduleList: List[CourseTableSchedule] = []


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
    midTerm: str = None
    endTerm: str = None
    usual: str = None
    makeUpScore: str = None
    makeUpScoreResult: str = None
    totalScore: str = None
    point: str = None


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
    id: str
    name: str = ''
    semester: str = ''
    activityDate: str = ''
    location: str = ''
    responsibility: str = ''
    loggingDateTime: str = ''
    status: str = ''
    comment: Union[str, None] = None


class QualityScholarship(BaseModel):
    id: str
    semester: str = ''
    activityType: str = ''
    activityContent: str = ''
    activityLevel: str = ''
    creditType: str = ''
    credit: str = ''


class Exam(BaseModel):
    code: str
    name: str = ''
    type: str = ''
    date: str = ''
    time: str = ''
    location: str = ''
    seatNumber: str = ''
    status: str = ''
    comment: str = ''


class PlanCommon(BaseModel):
    type: str = ''
    creditRequired: str = ''
    creditGained: str = ''
    result: str = ''
    status: str = ''
    comment: str = ''


class Plan(PlanCommon):
    code: str
    id: str = ''
    name: str = ''


class PlanGroup(PlanCommon):
    courseList: List[Plan] = []


class OtherExam(BaseModel):
    name: str
    result: str = ''
    status: str = ''
    semester: str = ''


# Public
class HelperMessage(BaseModel):
    notice: str = ''
    educationServerStatus: str = '未知'
    helperServerStatus: str = '未知'
    qualityServerStatus: str = '未知'
    week: str = ''
    semester: str = ''


class Notice(BaseModel):
    url: str
    title: str
    date: str
