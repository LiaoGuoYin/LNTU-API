import datetime

from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    username = Column(Integer, primary_key=True, index=True)
    password = Column(String(32))
    lastLogin = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    info = relationship("UserInfo")


class UserInfo(Base):
    __tablename__ = "user_info"

    username = Column(Integer, autoincrement=True, primary_key=True, index=True)
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
    enrollDate = Column(Date)
    graduateDate = Column(Date)
    chiefCollege = Column(String(32))  # TODO 转专业情况
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
