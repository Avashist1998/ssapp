import time
import heapq
import random
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from models import Event, EventStatus
from exceptions import EventNotFoundException, PlayerNotFoundException


class SSDataStore:
    """SS Datastore implementation"""
    def __init__(self):
        """SS datastore"""
        self.num_events_created = 0
        self.unix_time = time.mktime(datetime.now().timetuple())
        self.store: Dict[str, Event] = {}
        self.time_queue: List[Tuple[float, str]] = []

    def __get_santa_map(self, players: List[str]) -> Dict[str, str]:
        """Returns a lookup map for secrete santa"""
        _lookup = {}
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

    def get_events(self) -> List[Event]:
        """returns the list of events stored"""
        return self.store.values()


    def create_event(self, name:str,
                     date_time: datetime,
                     participants: List[str],
                     close_event: bool = False,
                     location: str = "") -> str:
        """Creates an event for our secret santa"""

        _id = str(self.num_events_created)
        event_state = EventStatus.OPEN
        santa_map = {}
        if close_event:
            santa_map = self.__get_santa_map(participants)
            event_state = EventStatus.CLOSED
        event = Event(_id, name, date_time, event_state, participants, santa_map, location)
        self.store[_id] = event
        date_time_float = time.mktime(date_time.timetuple())
        heapq.heappush(self.time_queue, (date_time_float, _id))
        self.num_events_created += 1
        return _id

    def get_event(self, event_id: str) -> Optional[Event]:
        """Get the event info"""

        if event_id in self.store:
            return self.store[event_id]
        return None

    def add_player(self, event_id: str, player: str):
        """adding a player to the game"""

        if event_id not in self.store:
            raise EventNotFoundException(event_id)
        elif self.store[event_id].event_status is not EventStatus.OPEN:
            raise ValueError(f"{event_id=} is no longer accepting players")
        else:
            self.store[event_id].event_participants.append(player)

    def close_event(self, event_id: str) -> None:
        """updates the status of the event to closed"""

        if event_id not in self.store:
            raise EventNotFoundException(event_id)
        elif self.store[event_id].event_status is EventStatus.EXPIRED:
            raise ValueError(f"{event_id=} has expired and cannot be closed")
        elif self.store[event_id].event_status is EventStatus.OPEN:
            self.store[event_id].event_santa_map = self.__get_santa_map(
                self.store[event_id].event_participants)
            self.store[event_id].event_status = EventStatus.CLOSED
        else:
            pass


    def remove_player(self, event_id: str, player: str):
        """remove player from a game"""
        if event_id not in self.store:
            raise EventNotFoundException(event_id)
        elif self.store[event_id].event_status is not EventStatus.OPEN:
            raise ValueError(f"{event_id=} is no longer accepting players")
        else:
            if player in self.store[event_id].event_participants:
                self.store[event_id].event_participants.remove(player)

    def get_player_secret_santa(self, event_id: str, user_name: str) -> str:
        """Get my secrete Santa Name"""
        # whether all player have unique names

        if event_id in self.store:
            if user_name in self.store[event_id].event_santa_map:
                return self.store[event_id].event_santa_map[user_name]
            raise PlayerNotFoundException(event_id, user_name)
        raise EventNotFoundException(event_id)

    def cancel_event(self, event_id) -> None:
        """Deletes the Event from store"""
        if event_id in self.store:
            _ = self.store.pop(event_id)