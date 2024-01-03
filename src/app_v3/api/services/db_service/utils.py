"""Database interface"""
from typing import List
from abc import ABC, abstractmethod

from db.models import Event, Player, Entry

class DataServiceException(Exception):
    """Data service exception"""
    def __init__(self, message: str):
        """Constructor"""
        self.message = message
        
class FailedDataServiceException(DataServiceException):
    """Failed data service exception"""
    def __init__(self, message: str):
        """Constructor"""
        self.message = message

class FailedToCreateException(DataServiceException):
    """Failed to create exception"""
    def __init__(self, message: str):
        """Constructor"""
        self.msg = message
        super().__init__(message)

class FailedToDeleteException(DataServiceException):
    """Failed to delete exception"""
    def __init__(self, message: str):
        """Constructor"""
        self.msg = message
        super().__init__(message)

class FailedToUpdateException(DataServiceException):
    """Failed to update exception"""
    def __init__(self, message: str):
        """Constructor"""
        self.msg = message
        super().__init__(message)

class FailedToGetException(DataServiceException):
    """Failed to get exception"""
    def __init__(self, message: str):
        """Constructor"""
        self.msg = message
        super().__init__(message)


class DataService(ABC):
    """DataStore interface"""


    @abstractmethod
    def add_player(self, player: Player):
        """Add a player to the database"""

    @abstractmethod
    def delete_player(self, email: str):
        """Delete a player from the database"""


    @abstractmethod
    def update_player(self, player: Player):
        """Update a player in the database"""

    @abstractmethod
    def get_player(self, email: str) -> Player:
        """Get a player from the database"""


    @abstractmethod
    def add_event(self, event: Event):
        """Add an event to the database"""

    @abstractmethod
    def delete_event(self, event_id: str):
        """Delete an event from the database"""

    @abstractmethod
    def update(self, event: Event):
        """Update an event in the database"""

    @abstractmethod
    def get_event(self, event_id: str) -> Event:
        """Get an event from the database"""

    @abstractmethod
    def add_entry(self, entry: Entry):
        """Add an entry to the database"""

    @abstractmethod
    def delete_entry(self, entry_id: str):
        """Delete an entry from the database"""

    @abstractmethod
    def update_entry(self, entry: Entry):
        """Update an entry in the database"""

    @abstractmethod
    def get_entry(self, entry_id: str):
        """Get an entry from the database"""

    @abstractmethod
    def get_entries(self, event_id: str = None, player_id: str = None) -> List[Entry]:
        """Get entries from the database"""

    @abstractmethod
    def get_events(self, page: int = 1, page_size:int = 10) -> List[Event]:
        """Get events from the database"""
