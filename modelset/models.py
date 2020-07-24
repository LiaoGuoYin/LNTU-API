from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

from sqlApp.database import Base


class User(Base):
    __tablename__ = "user"

    username = Column(Integer, primary_key=True, index=True)
    password = Column(String(32))

    grades = relationship("Grade", back_populates="owner")


class Grade(Base):
    __tablename__ = "grade"

    id = Column(Integer, primary_key=True)
    code = Column(String(32), index=True)
    name = Column(String(64), index=True)
    semester = Column(String(32))
    courseType = Column(String(32))
    credit = Column(String(32))
    grade = Column(String(32))
    usual = Column(String(32))
    midterm = Column(String(32))
    termEnd = Column(String(32))
    result = Column(String(32))
    ownerUsername = Column(Integer, ForeignKey('user.username'))

    owner = relationship("User", back_populates="grades")


class Notice(Base):
    __tablename__ = "notice"

    url = Column(String(255), primary_key=True, index=True)
    title = Column(String(255))
    date = Column(Date)
    content = Column(LONGTEXT)
    appendix = Column(Text)
