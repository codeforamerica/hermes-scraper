from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from common import Base

class CaseEventHistorical(Base):
    __tablename__ = 'case_events_historical'

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    datetime = Column(DateTime)
    title = Column(String)
    location = Column(String)
    inserted_on = Column(DateTime)
    latest = Column(Boolean)

    case = relationship("Case", backref=backref('historical_events', order_by=inserted_on))

    def __init__(self, case, when, title, location):
        self.case = case
        self.datetime = when
        self.title = title
        self.location = location
        self.latest = True
        self.inserted_on = datetime.now()
