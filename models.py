from sqlalchemy import Column, Integer, String, VARCHAR, DateTime, Boolean, LargeBinary
from database import Base
from datetime import datetime
from typing import List,Optional



class Song(Base):
    __tablename__ = 'song'

    ID = Column(Integer, primary_key=True, index=True, unique=True)
    Name = Column(VARCHAR(100))
    song = Column(VARCHAR(100))
    Duration = Column(Integer)
    Uploaded_time = Column(DateTime)


class Podcast(Base):

    __tablename__ = 'podcast'

    ID = Column(Integer, primary_key=True, index=True, unique=True)
    Name = Column(VARCHAR(100))
    Podcast = Column(VARCHAR(100))
    Duration = Column(Integer)
    Uploaded_time = Column(DateTime)
    Host = Column(VARCHAR(100))
    Participants = Column(VARCHAR(100))


class Audiobook(Base):

    __tablename__ = 'audiobook'

    ID = Column(Integer, primary_key=True, index=True, unique=True)
    Title = Column(VARCHAR(100))
    Author = Column(VARCHAR(100))
    Narrator = Column(VARCHAR(100))
    Duration = Column(Integer)
    Uploaded_time = Column(DateTime)
