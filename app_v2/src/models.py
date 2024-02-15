from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional

class EventStatus(Enum):
    """enum to track the state of the event"""
    OPEN=1
    CLOSED=2
    EXPIRED=3

class ConState(Enum):
    """enum to track the state of the UI"""
    MAIN=1
    QUIT=2
    EVENTS=0
    SS_EVENT=3
    NEW_EVENT=4
    ADD_PLAYER=5
    GET_EVENT=6
    CLOSE_EVENT=7
    DELETE_EVENT=8
    REMOVE_PLAYER=10
    DISPLAY=11

@dataclass
class Event:
    """Event data structure"""
    event_id: str
    event_name: str
    event_date_time: datetime
    event_status: EventStatus
    event_participants: List[str]
    event_santa_map: Dict[str, str]
    event_location: str = ""