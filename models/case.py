from sqlalchemy import Column, Integer, String, DateTime
from common import Base

class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    title = Column(String)
    inserted_on = Column(DateTime)
