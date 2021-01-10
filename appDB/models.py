import datetime

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    username = Column(String(64), primary_key=True, index=True)
    password = Column(String(128))
    qualityPassword = Column(String(128))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class UserInfo(Base):
    __tablename__ = "user_info"

    username = Column(String(64), primary_key=True, index=True)
    name = Column(String(64))
    photoURL = Column(String(128))
    nickname = Column(String(64))
    gender = Column(String(64))
    grade = Column(String(64))
    educationLast = Column(String(64))
    project = Column(String(64))
    education = Column(String(64))
    studentType = Column(String(64))
    college = Column(String(64))
    major = Column(String(64))
    direction = Column(String(64))
    enrollDate = Column(String(64))
    graduateDate = Column(String(64))
    chiefCollege = Column(String(64))
    studyType = Column(String(64))
    membership = Column(String(64))
    isInSchool = Column(String(64))
    campus = Column(String(64))
    majorClass = Column(String(64))
    effectAt = Column(String(64))
    isInRecord = Column(String(64))
    studentStatus = Column(String(64))
    isWorking = Column(String(64))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class CourseTable(Base):
    __tablename__ = "course_table"

    username = Column(String(64), primary_key=True, index=True)
    semester = Column(String(64), primary_key=True, index=True)
    code = Column(String(64), primary_key=True, index=True)
    name = Column(String(128))
    teacher = Column(String(64))
    credit = Column(String(64))
    scheduleList = Column(JSON)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Exam(Base):
    __tablename__ = "exam"

    username = Column(String(64), primary_key=True, index=True)
    code = Column(String(64), primary_key=True, index=True)
    name = Column(String(128))
    type = Column(String(64))
    date = Column(String(64))
    time = Column(String(64))
    location = Column(String(64))
    seatNumber = Column(String(64))
    status = Column(String(64))
    comment = Column(String(64))
    semester = Column(String(64))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Grade(Base):
    __tablename__ = "grade"

    username = Column(String(64), primary_key=True, index=True)
    code = Column(String(64), primary_key=True, index=True)
    name = Column(String(128))
    semester = Column(String(64))
    courseType = Column(String(64))
    credit = Column(String(64))
    usual = Column(String(64))
    midTerm = Column(String(64))
    endTerm = Column(String(64))
    makeUpScore = Column(String(64))
    makeUpScoreResult = Column(String(64))
    totalScore = Column(String(64))
    result = Column(String(64))
    point = Column(String(64))
    status = Column(String(64))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class AiPaoOrder(Base):
    __tablename__ = "aipao_order"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(64))
    name = Column(String(64))
    gender = Column(String(64))
    schoolName = Column(String(64))
    successCount = Column(Integer)
    failureCount = Column(Integer)

    isCodeValid = Column(Boolean)
    isDoneToday = Column(Boolean)

    IMEI = Column(String(64))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Classroom(Base):
    __tablename__ = "public_classroom"

    buildingName = Column(String(64))
    week = Column(String(64), primary_key=True, index=True)
    room = Column(String(64), primary_key=True, index=True)
    type = Column(String(64))
    capacity = Column(String(64))
    scheduleList = Column(JSON)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Notice(Base):
    __tablename__ = "public_notice"

    title = Column(String(64), primary_key=True)
    url = Column(String(64), primary_key=True)
    date = Column(String(64), index=True)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class QualityActivity(Base):
    __tablename__ = "quality_activity"

    username = Column(String(64), primary_key=True, index=True)
    type = Column(String(64), primary_key=True)
    id = Column(String(64), primary_key=True)
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
    __tablename__ = "notification_subscription"

    token = Column(String(128), primary_key=True, index=True)
    username = Column(String(64))
    isNotice = Column(Boolean, default=False)
    isGrade = Column(Boolean, default=False)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
