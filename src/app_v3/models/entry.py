"""Entry model"""
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

from typing import Optional
from event import Event
from player import Player

class EntryBase(BaseModel):
    """Entry model"""
    event_id: int = Field(immutable=True)
    player_email: str = Field(immutable=True)
    ss_recipient_email: Optional[Annotated[str, Field(immutable=False,
                                                      default_factory=None,
                                                      Optional=True)]] = None
class EntryCreate(EntryBase):
    """Create entry model"""

class Entry(EntryBase):
    """Entry model"""
    id: int = Field(alias='_id', immutable=True)
    
    event: Optional[Event] = None
    player: Optional[Player] = None

    model_config = ConfigDict(from_attributes=True)