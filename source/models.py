from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    created_at = Column(DateTime(timezone=True))
