import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    username = Column(String(32), primary_key=True, index=True)
    password = Column(String(32))

    lastLogin = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class UserInfo(Base):
    __tablename__ = "user_info"

    username = Column(String(32), primary_key=True, index=True)
    name = Column(String(32))
    photoUrl = Column(String(128))
    nickname = Column(String(32))
    gender = Column(String(32))
    grade = Column(String(32))
    educationLast = Column(String(32))
    project = Column(String(32))
    education = Column(String(32))
    studentType = Column(String(32))
    college = Column(String(32))
    major = Column(String(32))
    direction = Column(String(32))
    enrollDate = Column(String(32))
    graduateDate = Column(String(32))
    chiefCollege = Column(String(32))
    studyType = Column(String(32))
    membership = Column(String(32))
    isInSchool = Column(String(32))
    campus = Column(String(32))
    majorClass = Column(String(32))
    effectAt = Column(String(32))
    isInRecord = Column(String(32))
    studentStatus = Column(String(32))
    isWorking = Column(String(32))

    lastCalculateTime = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class CourseTable(Base):
    __tablename__ = "course_table"

    code = Column(String(32), primary_key=True, index=True)
    name = Column(String(128))
    teacher = Column(String(16))
    credit = Column(String(16))
    schedules = Column(JSON)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Grade(Base):
    __tablename__ = "grade"

    username = Column(String(32), primary_key=True, index=True)
    code = Column(String(32), primary_key=True, index=True)
    name = Column(String(128))
    semester = Column(String(32))
    courseType = Column(String(32))
    grade = Column(String(32))
    credit = Column(String(32))
    usual = Column(String(32))
    midTerm = Column(String(32))
    endTerm = Column(String(32))
    makeUpScore = Column(String(32))
    makeUpScoreResult = Column(String(32))
    result = Column(String(32))
    point = Column(String(32))
    status = Column(String(32))

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class GPA(Base):
    __tablename__ = "gpa"

    username = Column(String(32), primary_key=True, index=True)
    semester = Column(String(32), primary_key=True, index=True)
    gradePointAverage = Column(Float(precision=8, decimal_return_scale=2))
    weightedAverage = Column(Float(precision=8, decimal_return_scale=2))
    gradePointTotal = Column(Float)
    scoreTotal = Column(Float)
    creditTotal = Column(Float)
    courseCount = Column(Integer)

    lastCalculateTime = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class AiPaoOrder(Base):
    __tablename__ = "aipao_order"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(64))
    name = Column(String(64))
    gender = Column(String(32))
    schoolName = Column(String(64))
    successCount = Column(Integer)
    failureCount = Column(Integer)

    isCodeValid = Column(Boolean)
    isDoneToday = Column(Boolean)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
