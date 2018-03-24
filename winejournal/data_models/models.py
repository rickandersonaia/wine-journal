from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.settings import SQLALCHEMY_DATABASE_URI

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)