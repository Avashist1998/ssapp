from sqlite_db import Base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base




class Player(Base):
    """Player model"""
    __tablename__ = "players"

    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)

class Event(Base):
    """Event model"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    creator = ForeignKey(Player.email, index=True)
    location = Column(String, nullable=True, default=None, index=False)

    limit = Column(Integer, nullable=False, default=0, index=False)
    price = Column(Integer, nullable=False, default=0, index=False)
    public = Column(Boolean, nullable=False, default=True, index=False)
    locked = Column(Boolean, nullable=False, default=False, index=False)

    rsvp_date = Column(DateTime, nullable=False, index=False)
    event_date = Column(DateTime, nullable=False, index=False)
    created_date = Column(DateTime, nullable=False, index=False)


class Entry(Base):
    """Entry model"""
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    event_id = ForeignKey(Event.id, index=True)
    player_email = ForeignKey(Player.email, index=True)
    ss_recipient_email = ForeignKey(Player.email, nullable=True, default=None, index=True)
