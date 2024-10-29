#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Define the base for models
Base = declarative_base()

# Define Event and Participant models
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    creator_id = Column(Integer, nullable=False)
    is_private = Column(Boolean, default=False)
    event_date = Column(DateTime)
    expiry_date = Column(DateTime)
    archive_after_expiry = Column(Boolean, default=True)
    role_id = Column(Integer, nullable=True)  # Only for private events

class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    user_id = Column(Integer, nullable=False)

# Function to create the database engine and session
def get_session(database_url="sqlite:///events.db"):
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
