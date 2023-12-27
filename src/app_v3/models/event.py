"""Event model"""
import datetime
from typing import List, Tuple, Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field


class Event(BaseModel):
    """Event model"""
    id: int = Field(alias='_id', immutable=True)
    name: str
    creator: str = Field(immutable=True)
    location: Optional[Annotated[str, Field(immutable=False)]] = None

    limit: int = Field(default=0, immutable=False)
    price: float = Field(default=0.0, immutable=False)
    public: bool = Field(default=False, immutable=True)
    locked: bool = Field(default=False, immutable=False)

    rsvp_date: datetime.datetime = Field(immutable=False)
    event_date: datetime.datetime = Field(immutable=False)
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow,
                                            immutable=True)

    participants: List[str] = Field(default_factory=list, immutable=False, Optional=True)
    ss_map: List[Tuple[str, str]] = Field(default_factory=list, immutable=False, Optional=True)
