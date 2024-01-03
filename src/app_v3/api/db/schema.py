"""Database Schemas"""
from datetime import datetime
from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped

from db.base import Base

class PlayerORM(Base):
    """Player model"""
    __tablename__ = "players"

    name = Column(String, index=True)
    email = Column(String, unique=True, primary_key=True, index=True)
    created_date = Column(DateTime, nullable=False, index=False, default=datetime.now())

    entries: Mapped[List["EntryORM"]] = relationship("EntryORM",
                                                     foreign_keys="EntryORM.player_email")


class EventORM(Base):
    """Event model"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    creator = Column(String, ForeignKey(PlayerORM.email))
    location = Column(String, nullable=True, default=None, index=False)

    limit = Column(Integer, nullable=False, default=0, index=False)
    price = Column(Integer, nullable=False, default=0, index=False)
    public = Column(Boolean, nullable=False, default=True, index=False)
    locked = Column(Boolean, nullable=False, default=False, index=False)

    rsvp_date = Column(DateTime, nullable=False, index=False)
    event_date = Column(DateTime, nullable=False, index=False)
    created_date = Column(DateTime, nullable=False, index=False, default=datetime.now())

    entries: Mapped[List["EntryORM"]] = relationship("EntryORM", foreign_keys="EntryORM.event_id")


class EntryORM(Base):
    """Entry model"""
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    player_email = Column(Integer, ForeignKey("players.email"))
    created_date = Column(DateTime, nullable=False, index=False, default=datetime.now())
    ss_recipient_email = Column(Integer, ForeignKey("players.email"), nullable=True, default=None, index=False)

    