from sqlalchemy import Column, Integer, String, ForeignKey
from common import Base

class CaseEventsLatest(Base):
    __tablename__ = 'case_events_latest'

    id = Column(Integer, ForeignKey('case_events_historical.id'), primary_key=True)
