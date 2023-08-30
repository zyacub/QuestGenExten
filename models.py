from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.dialects.postgresql import JSONB
from config import Base


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    data = Column(JSONB)
    