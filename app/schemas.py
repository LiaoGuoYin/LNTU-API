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
    message: str = 'Success'
    data: Union[list, dict, None] = None


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
# For Education and Quality commonly using
class User(BaseModel):
    username: str
    password: str


# UserInfo
class UserInfo(BaseModel):
    username: str
    name: str
    photoURL: str = ''
    nickname: str = ''
    gender: str = ''
    grade: str = ''
    educationLast: str = ''
    project: str = ''
    education: str = ''
    studentType: str = ''
    college: str = ''
    major: str = ''
    direction: Union[str, None] = ''
    enrollDate: str = ''
    graduateDate: str = ''
    chiefCollege: str = ''
    studyType: str = ''
    membership: str = ''
    isInSchool: str = ''
    campus: str = ''
    majorClass: str = ''
    effectAt: str = ''
    isInRecord: str = ''
    studentStatus: str = ''
    isWorking: str = ''


# CourseTable
class CourseTableSchedule(BaseModel):
    room: str = ''
    weekday: int = 1  # TODO
    index: int = 1
    weeksString: str = ''
    weeks: Union[list, None] = []


class CourseTable(BaseModel):
    code: str
    name: str = ''
    teacher: str = ''
    credit: str = ''
    scheduleList: List[CourseTableSchedule] = []


# GradeTable
class GradeTable(BaseModel):
    class CourseStatusEnum(str, Enum):
        normal = "正常"
        makeUp = "补考"
        reStudy = "重修"

    name: str
    credit: str = ''
    semester: str = ''
    status: CourseStatusEnum = CourseStatusEnum.normal
    result: str = ''


# Grade
class Grade(GradeTable):
    code: str
    courseType: str = ''
    midTerm: str = ''
    endTerm: str = ''
    usual: str = ''
    makeUpScore: Union[str, None] = None
    makeUpScoreResult: Union[str, None] = None
    totalScore: str = ''
    point: str = ''


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
    title: str = ''
    date: str = ''


# Quality
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


# Data
class EducationDataResponse(BaseModel):
    info: UserInfo
    courseTable: List[CourseTable] = []
    exam: List[Exam] = []
    grade: List[Grade] = []
