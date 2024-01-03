"""Event model"""
import datetime
from typing import List, Tuple, Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict

from models.entry import Entry

class EventBase(BaseModel):
    """Event Base model"""
    name: str
    creator: str = Field(immutable=True)
    location: Optional[Annotated[str, Field(immutable=False)]] = None
    limit: int = Field(default=0, immutable=False)
    price: float = Field(default=0.0, immutable=False)
    public: bool = Field(default=False, immutable=True)
    locked: bool = Field(default=False, immutable=False)
    rsvp_date: datetime.datetime = Field(immutable=False)
    event_date: datetime.datetime = Field(immutable=False)

class EventCreate(EventBase):
    """Create event model"""
    pass

class Event(EventBase):
    """Event model"""
    id: int = Field(alias='id', immutable=True)
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow,
                                            immutable=True)

    entries: List["Entry"] = []
    model_config = ConfigDict(from_attributes=True)
