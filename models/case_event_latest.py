from sqlalchemy import Column, Integer, String, ForeignKey
from common import Base

class CaseEventLatest(Base):
    __tablename__ = 'case_events_latest'

    id = Column(Integer, ForeignKey('case_event_historical.id'), primary_key=True)
