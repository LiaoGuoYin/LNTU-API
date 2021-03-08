import datetime

from sqlalchemy import Column, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    username = Column(String(128), primary_key=True, index=True)
    password = Column(String(128))
    qualityPassword = Column(String(128))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class UserInfo(Base):
    __tablename__ = "info"

    username = Column(String(128), primary_key=True, index=True)
    name = Column(String(128))
    photoURL = Column(String(128))
    nickname = Column(String(128))
    gender = Column(String(128))
    grade = Column(String(128))
    educationLast = Column(String(128))
    project = Column(String(128))
    education = Column(String(128))
    studentType = Column(String(128))
    college = Column(String(128))
    major = Column(String(128))
    direction = Column(String(128))
    enrollDate = Column(String(128))
    graduateDate = Column(String(128))
    chiefCollege = Column(String(128))
    studyType = Column(String(128))
    membership = Column(String(128))
    isInSchool = Column(String(128))
    campus = Column(String(128))
    majorClass = Column(String(128))
    effectAt = Column(String(128))
    isInRecord = Column(String(128))
    studentStatus = Column(String(128))
    isWorking = Column(String(128))
    address = Column(String(128))
    train = Column(String(128))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class CourseTable(Base):
    __tablename__ = "course"

    username = Column(String(128), primary_key=True, index=True)
    semester = Column(String(128), primary_key=True, index=True)
    code = Column(String(128), primary_key=True, index=True)
    name = Column(String(128))
    teacher = Column(String(128))
    credit = Column(String(128))
    scheduleList = Column(JSON)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Exam(Base):
    __tablename__ = "exam"

    username = Column(String(128), primary_key=True, index=True)
    code = Column(String(128), primary_key=True, index=True)
    name = Column(String(128))
    type = Column(String(128), primary_key=True)
    date = Column(String(128))
    time = Column(String(128))
    location = Column(String(128))
    seatNumber = Column(String(128))
    status = Column(String(128))
    comment = Column(String(128))
    semester = Column(String(128))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Grade(Base):
    __tablename__ = "grade"

    username = Column(String(128), primary_key=True, index=True)
    code = Column(String(128), primary_key=True, index=True)
    name = Column(String(128), primary_key=True, index=True)
    semester = Column(String(128))
    courseType = Column(String(128))
    credit = Column(String(128))
    usual = Column(String(128))
    midTerm = Column(String(128))
    endTerm = Column(String(128))
    makeUpScore = Column(String(128))
    makeUpScoreResult = Column(String(128))
    totalScore = Column(String(128))
    result = Column(String(128))
    point = Column(String(128))
    status = Column(String(128))
    isPushed = Column(Boolean, default=True)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Classroom(Base):
    __tablename__ = "classroom"

    buildingName = Column(String(128))
    week = Column(String(128), primary_key=True, index=True)
    room = Column(String(128), primary_key=True, index=True)
    type = Column(String(128))
    capacity = Column(String(128))
    scheduleList = Column(JSON)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Notice(Base):
    __tablename__ = "notice"

    title = Column(String(128), primary_key=True)
    url = Column(String(128))
    date = Column(String(128), primary_key=True)
    isPushed = Column(Boolean, default=True)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class QualityActivity(Base):
    __tablename__ = "quality"

    username = Column(String(128), primary_key=True, index=True)
    type = Column(String(128), primary_key=True)
    id = Column(String(128), primary_key=True)
    name = Column(String(255), primary_key=True)
    semester = Column(String(255))
    activityDate = Column(String(255))
    location = Column(String(255))
    responsibility = Column(String(255))
    loggingDateTime = Column(String(255))
    status = Column(String(255))
    comment = Column(String(255))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class NotificationToken(Base):
    __tablename__ = "subscription"

    token = Column(String(128), primary_key=True, index=True)
    username = Column(String(128))
    isSubscribeNotice = Column(Boolean, default=True)
    isSubscribeGrade = Column(Boolean, default=True)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
