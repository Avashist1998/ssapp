class QuitException(Exception):
    """Defining exit exception"""
    def __init__(self, msg:str):
        self.msg = msg

class EventNotFoundException(Exception):
    """Define event not found exception"""
    def __init__(self, event_id:str):
        self.msg = f"{event_id=} not found in system"

class PlayerNotFoundException(Exception):
    """Define PlayerNotFound"""
    def __init__(self, event_id: str, player:str):
        self.msg = f"{player=} not found in {event_id=}."
