"""base meta class"""
from sqlalchemy.ext.declarative import declarative_base, api


Base: api.DeclarativeMeta = declarative_base()
