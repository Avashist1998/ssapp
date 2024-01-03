"""Model"""
import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from typing import Optional, List, Tuple

class EntryBase(BaseModel):
    """Entry model"""
    event_id: int = Field(immutable=True)
    player_email: str = Field(immutable=True)

class EntryCreate(EntryBase):
    """Create entry model"""

class Entry(EntryBase):
    """Entry model"""
    id: int = Field(alias='id', immutable=True)
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow,
                                            immutable=True)
    ss_recipient_email: Optional[Annotated[str, Field(immutable=False,
                                                        default_factory=None,
                                                        Optional=True)]] = None
    model_config = ConfigDict(from_attributes=True)

class EventBase(BaseModel):
    """Event Base model"""
    name: str
    creator: str = Field(immutable=True)
    location: Optional[Annotated[str, Field(immutable=False)]] = None
    limit: Optional[Annotated[int, Field(default=None, immutable=False)]] = None
    price: float = Field(default=0.0, immutable=False)
    public: bool = Field(default=True, immutable=True)
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

class PlayerBase(BaseModel):
    """Player Base model"""

    name: str = Field(immutable=False)
    email: str = Field(immutable=True)


class PlayerCreate(PlayerBase):
    """Create player model"""

class Player(PlayerBase):
    """Player model"""
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow,
                                            immutable=True)

    entries: List[Entry] = []
    model_config = ConfigDict(from_attributes=True)