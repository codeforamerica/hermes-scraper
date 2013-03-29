import db.connection
from models import *

common.Base.metadata.create_all(db.connection.engine) 
