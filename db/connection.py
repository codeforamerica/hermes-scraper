from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://hermes_scraper@localhost/hermes')
Session = sessionmaker(bind=engine)
