"""Entry model"""
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from typing import Optional

class Entry(BaseModel):
    """Entry model"""
    id: int = Field(alias='_id', immutable=True)
    event_id: str = Field(immutable=True)
    player_email: str = Field(immutable=True)
    ss_recipient_email: Optional[Annotated[str, Field(immutable=False,
                                                      default_factory=None,
                                                      Optional=True)]] = None
