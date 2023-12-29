"""Player model"""
import datetime
from typing import List

from models.entry import Entry
from pydantic import BaseModel, Field, ConfigDict

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
