from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import scoped_session, sessionmaker

# Hardcoded credentials - PLEASE DON'T DO THIS IN PRODUCTION
USER = "hbnb_evo_2"
PWD = "hbnb_evo_2_pwd"
HOST = "0.0.0.0"
DB = "hbnb_evo_2_db"

Base = declarative_base()

engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(USER, PWD, HOST, DB))
session_factory = sessionmaker(
    bind=engine, expire_on_commit=False)
session = scoped_session(session_factory)

db_session = session()

from app.models.user import User
from app.models.place import Place

Base.metadata.create_all(engine)
