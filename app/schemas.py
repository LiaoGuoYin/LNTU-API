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

    educationUsername: str
    educationPassword: str
    qualityUsername: str
    qualityPassword: str

    bundleId: str = ''
    teamId: str = ''
    keyId: str = ''
    keyPath: str = ''


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
    name: str = ''
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
    direction: str = ''
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
    address: str = ''
    train: str = ''


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


class TeacherEvaluationRequest(User):
    submit: bool = False


class TeacherEvaluationResponse(BaseModel):
    code: str
    name: str = ''
    teacher: str = ''
    status: str = ''
    id: str = ''


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


class NotificationSubscriptionEnum(Enum):
    GRADE = 'GRADE'
    NOTICE = 'NOTICE'
    ADMIN = 'ADMIN'

    @classmethod
    def values(cls):
        return [each.value for each in cls]


# Apple Push Notification Token
class NotificationToken(BaseModel):
    token: str
    username: str
    subscriptionList: List[NotificationSubscriptionEnum] = []

    class Config:
        schema_extra = {
            "example": {
                "token": "test-token",
                "username": "1700000000",
                "subscriptionList": NotificationSubscriptionEnum.values()
            }
        }


class NotificationPushBaseModel(BaseModel):
    token: str


# Notice Push
class NoticePushNotification(NotificationPushBaseModel):
    contentBody: str = ''


# Grade Push
class GradePushNotification(NotificationPushBaseModel):
    username: str
    courseName: str
    courseResult: str
    isPushed: bool = False

    @property
    def contentBody(self):
        """GPA计算规则:
           "二级制: 合格(85),不合格(0)"
           "五级制: 优秀(95),良(85),中(75),及格(65),不及格(0)"
       """
        if self.courseResult.isdigit():
            content_body = '好像没发挥好噢，加油加油!' if float(self.courseResult) < 60.0 else '还不错噢，继续努力!'
        else:
            content_body = '好像没发挥好噢，加油加油!' if '不' in self.courseResult else '还不错噢，继续努力!'

        return f'{self.courseName}: {self.courseResult}，{content_body}'
