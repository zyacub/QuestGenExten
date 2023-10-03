from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from config import Base


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    data = Column(JSONB)

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    questions = Column(JSONB)
    helpful = Column(JSONB)
    