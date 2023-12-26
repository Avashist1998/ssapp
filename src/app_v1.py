"""App V1 Implementation"""
import uuid
import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class Event:
    """Event data structure"""
    event_id: str
    event_name: str
    event_date_time: datetime
    event_participants: List[str]
    event_santa_map: Dict[str, str]
    event_location: str = ""

class EventNotFoundException(Exception):
    """Define event not found exception"""
    def __init__(self, event_id:str):
        self.msg = f"{event_id=} not found in system"

class PlayerNotFoundException(Exception):
    """Define PlayerNotFound"""
    def __init__(self, event_id: str, player:str):
        self.msg = f"{player=} not found in {event_id=}."

class NotEnoughPlayersException(Exception):
    """Define NotEnoughPlayers"""
    def __init__(self, event_name: str):
        self.msg = f"{event_name=} cannot created because it does not have enough players to play"

class SSApp:
    """Secret Santa Application"""

    def __init__(self):
        """SS Application constructor"""
        self.store: Dict[str, Event] = {}

    def __get_santa_map(self, players: List[str]) -> Dict[str, str]:
        """Returns a lookup map for secrete santa"""

        if len(players) < 2:
            raise NotEnoughPlayersException("")

        _lookup: Dict[str, str] = {}
        _choices = set(players)
        for player in players:
            remove_self = False
            if player in _choices:
                _choices.remove(player)
                remove_self = True
            pick = random.choice(list(_choices))
            if remove_self:
                _choices.add(player)

            _choices.remove(pick)
            _lookup[player] = pick
        return _lookup

    def create_event(self, name:str,
                     date_time: datetime,
                     participants: List[str],
                     location: Optional[str] = "") -> str:
        """Creates an event for our secret santa"""

        _id = uuid.uuid4()
        while _id in self.store:
            _id = uuid.uuid4()
        try:
            santa_map = self.__get_santa_map(participants)
        except NotEnoughPlayersException as err:
            raise NotEnoughPlayersException(name) from err
        event = Event(str(_id), name, date_time, participants, santa_map, location)
        self.store[str(_id)] = event
        return str(_id)

    def get_event_info(self, event_id: str) -> Optional[Event]:
        """Get the event info"""

        if event_id in self.store:
            return self.store[event_id]
        return None

    def get_player_ss(self, event_id: str, player: str) -> str:
        """Get player secrete Santa Name"""

        if event_id in self.store:
            if player in self.store[event_id].event_santa_map:
                return self.store[event_id].event_santa_map[player]
            raise PlayerNotFoundException(event_id, player)
        raise EventNotFoundException(event_id)

    def cancel_event(self, event_id) -> None:
        """Deletes the event from store"""

        if event_id in self.store:
            _ = self.store.pop(event_id)
