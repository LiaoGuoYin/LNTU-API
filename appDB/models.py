import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    username = Column(Integer, primary_key=True, index=True)
    password = Column(String(32))
    lastLogin = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    info = relationship("UserInfo")
    grade_table = relationship("GradeTable")


class UserInfo(Base):
    __tablename__ = "user_info"

    username = Column(Integer, primary_key=True, index=True)
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
    enrollDate = Column(String(16))
    graduateDate = Column(String(16))
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

    # Foreign key
    ownerUsername = Column(Integer, ForeignKey(User.username))


class GradeTable(Base):
    __tablename__ = "grade_table"

    username = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), primary_key=True, index=True)
    credit = Column(String(16))
    result = Column(String(16))
    semester = Column(String(16), primary_key=True)
    status = Column(String(16))

    # Foreign key
    ownerUsername = Column(Integer, ForeignKey(User.username))


class GPA(Base):
    __tablename__ = "gpa"

    username = Column(Integer, primary_key=True, index=True)
    semester = Column(String(16), primary_key=True, index=True)
    gradePointAverage = Column(Float(precision=8, decimal_return_scale=2))
    weightedAverage = Column(Float(precision=8, decimal_return_scale=2))
    gradePointTotal = Column(Float)
    scoreTotal = Column(Float)
    creditTotal = Column(Float)
    courseCount = Column(Integer)
    lastCalculateTime = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # Foreign key
    ownerUsername = Column(Integer, ForeignKey(User.username))


class Grade(Base):
    __tablename__ = "grade"

    username = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), primary_key=True, index=True)
    name = Column(String(128))
    semester = Column(String(16))
    courseType = Column(String(16))
    grade = Column(String(16))
    credit = Column(String(16))
    usual = Column(String(16))
    midTerm = Column(String(16))
    endTerm = Column(String(16))
    makeUpScore = Column(String(16))
    makeUpScoreResult = Column(String(16))
    result = Column(String(16))
    point = Column(String(16))
    status = Column(String(16))
    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # Foreign key
    ownerUsername = Column(Integer, ForeignKey(User.username))


class CourseTable(Base):
    __tablename__ = "course_table"

    code = Column(String(32), primary_key=True, index=True)
    name = Column(String(128))
    teacher = Column(String(16))
    credit = Column(String(16))
    schedules = Column(JSON)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class AiPaoOrder(Base):
    __tablename__ = "aipao_order"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32))
    name = Column(String(32))
    gender = Column(String(32))
    schoolName = Column(String(32))
    successCount = Column(Integer)
    failureCount = Column(Integer)

    isCodeValid = Column(Boolean)
    isDoneToday = Column(Boolean)

    lastUpdatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
