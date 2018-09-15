from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME, INTEGER, TEXT
from sqlalchemy.orm import relationship

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key = True, nullable = False)
    tag = Column(TEXT)

class Record(Base):
    __tablename__ = 'record'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key = True, nullable = False)
    title = Column(TEXT)
    content = Column(TEXT)

class Tags(Base):
    __tablename__ = 'tags'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key = True, nullable = False)
    parent_id = Column(INTEGER, ForeignKey('record.id'))
    tag_id = Column(INTEGER, ForeignKey('tag.id'))

class Event(Base):
    __tablename__ = 'event'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(TEXT)
    server = Column(TEXT)
    date = Column(DATETIME)


class Attendance(Base):
    __tablename__ = 'attendance'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key=True, nullable=False)
    member_id = Column(TEXT)
    event_id = Column(TEXT)


class Member(Base):
    __tablename__ = 'member'
    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(TEXT)
    avatar = Column(TEXT)