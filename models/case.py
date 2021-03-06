from sqlalchemy import Column, Integer, String, DateTime
from common import Base
from datetime import datetime

class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    title = Column(String)
    inserted_on = Column(DateTime)

    def __init__(self, number, title):
        self.number = number
        self.title = title
        self.inserted_on = datetime.now()
