"""Player model"""
from pydantic import BaseModel, Field


class Player(BaseModel):
    """Player model"""

    name: str = Field(immutable=True)
    email: str = Field(immutable=False)
