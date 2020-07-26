import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    username = Column(Integer, primary_key=True, index=True)
    password = Column(String(32))
    lastLogin = Column(Date, default=datetime.datetime.now())

    info = relationship("UserInfo", back_populates="user")


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(Integer)
    name = Column(String(32))
    photoUrl = Column(String(128))
    nickname = Column(String(32))
    gender = Column(String(32))
    grade = Column(String(32))
    education_last = Column(String(32))
    project = Column(String(32))
    education = Column(String(32))
    studentType = Column(String(32))
    college = Column(String(32))
    major = Column(String(32))
    direction = Column(String(32))
    enrollDate: datetime.date
    graduateDate: datetime.date
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
    owner_username = Column(Integer, ForeignKey(User.username))
    owner = relationship("User", back_populates="info")
