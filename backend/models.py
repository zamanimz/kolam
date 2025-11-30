from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class PondLog(Base):
    __tablename__ = "pond_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ph = Column(Float)
    ec = Column(Float)
    do = Column(Float)
    temp = Column(Float)
