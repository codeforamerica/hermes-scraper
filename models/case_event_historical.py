from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from common import Base

class CaseEventHistorical(Base):
    __tablename__ = 'case_events_historical'

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    datetime = Column(DateTime)
    title = Column(String)
    location = Column(String)
    inserted_on = Column(DateTime)

    case = relationship("Case", backref=backref('historical_events', order_by=inserted_on))
