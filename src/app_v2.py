"""Version 2 of the Secret Santa application"""
import uuid
import time
import os
import random
import heapq
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

class EventStatus(Enum):
    """enum to track the state of the event"""
    OPEN=1
    CLOSED=2
    EXPIRED=3


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

class SSApp:
    """Secrete Santa Application"""

    def __init__(self):
        self.con_state = ConState.MAIN
        self.store = SSDataStore()
        self.cli = SSCli()

        self.player = ""
        self.event_id = ""
        self.event_name = ""
        self.event_time = ""
        self.event_status = None
        self.event_location = None
        self.event_participants = None

    def clear_input_buffer(self):
        """Clears the input buffer"""
        self.player = ""
        self.event_id = ""
        self.event_name = ""
        self.event_time = ""
        self.event_status = None
        self.event_location = None
        self.event_participants = None


    def validate_main_input(self, choice: str) -> ConState:
        """validate the main input"""
        choice_to_conv_state = {
            "n": ConState.NEW_EVENT,
            "g": ConState.GET_EVENT,
            "a": ConState.ADD_PLAYER,
            "r": ConState.REMOVE_PLAYER, 
            "c": ConState.CLOSE_EVENT, 
            "d": ConState.DELETE_EVENT,
            "s": ConState.SS_EVENT,
            "q": ConState.QUIT,
            "l": ConState.EVENTS,
        }

        if choice not in choice_to_conv_state:
            self.cli.invalid_input_msg()
            return self.con_state
        return choice_to_conv_state[choice]


    def validate_global(self, choice: str) -> ConState:
        """Only can go to some values"""
        choice_to_gol_state = {
            "m": ConState.MAIN,
            "q": ConState.QUIT,
            "l": ConState.EVENTS
        }

        if choice in choice_to_gol_state:
            return choice_to_gol_state[choice]
        return ConState.MAIN
    def run(self):
        """run the user interface"""
        while True:
            try:
                if self.con_state is ConState.MAIN:
                    self.cli.clear_screen()
                    self.cli.dis_header_message()
                    choice = self.cli.get_main_choices()
                    self.con_state = self.validate_main_input(choice)

                elif self.con_state is ConState.EVENTS:
                    self.cli.clear_screen()
                    events = self.store.get_events()
                    self.cli.dis_events(events)
                    self.con_state = ConState.DISPLAY

                elif self.con_state is ConState.DELETE_EVENT:
                    if self.event_id == "":
                        self.cli.clear_screen()
                        self.event_id = self.cli.get_event_id()
                    else:
                        self.store.cancel_event(self.event_id)
                        self.cli.dis_cancel_event_msg(self.event_id)
                        self.con_state = ConState.DISPLAY
                        self.clear_input_buffer()

                elif self.con_state is ConState.GET_EVENT:
                    if self.event_id == "":
                        self.cli.clear_screen()
                        self.event_id = self.cli.get_event_id()
                    else:
                        event = self.store.get_event(self.event_id)
                        if event:
                            self.cli.dis_event_info(event)
                        else:
                            self.cli.dis_event_not_found(self.event_id)
                        self.con_state = ConState.DISPLAY
                        self.clear_input_buffer()

                elif self.con_state is ConState.ADD_PLAYER:
                    if self.event_id == "":
                        self.cli.clear_screen()
                        self.event_id = self.cli.get_event_id()
                    elif self.player == "":
                        self.player = self.cli.get_player_name()
                    else:
                        try:
                            self.store.add_player(self.event_id, self.player)
                            self.cli.dis_event_info(self.store.get_event(self.event_id))
                            self.cli.dis_event_update_msg(self.event_id)
                        except EventNotFoundException as err:
                            self.cli.dis_error(err.msg)
                        except ValueError as _:
                            self.cli.dis_event_close_msg(self.event_id)
                        self.clear_input_buffer()
                        self.con_state = ConState.DISPLAY

                elif self.con_state is ConState.REMOVE_PLAYER:
                    if self.event_id == "":
                        self.cli.clear_screen()
                        self.event_id = self.cli.get_event_id()
                    elif self.player == "":
                        self.player = self.cli.get_player_name()
                    else:
                        try:
                            self.store.remove_player(self.event_id, self.player)
                            self.cli.dis_event_info(self.store.get_event(self.event_id))
                            self.cli.dis_event_update_msg(self.event_id)
                        except ValueError as _:
                            self.cli.dis_event_close_msg(self.event_id)
                        self.clear_input_buffer()
                        self.con_state = ConState.DISPLAY
                elif self.con_state is ConState.CLOSE_EVENT:
                    if self.event_id == "":
                        self.cli.clear_screen()
                        self.event_id = self.cli.get_event_id()
                    else:
                        try:
                            self.store.close_event(self.event_id)
                            self.cli.dis_event_close_msg(self.event_id)
                        except EventNotFoundException as err:
                            self.cli.dis_error(err.msg)
                        self.con_state = ConState.DISPLAY
                        self.event_id = ""
                elif self.con_state is ConState.NEW_EVENT:
                    if self.event_name == "":
                        self.cli.clear_screen()
                        self.event_name = self.cli.get_event_name()
                    elif self.event_location is None:
                        self.event_location = self.cli.get_location()
                    elif self.event_participants is None:
                        self.event_participants = self.cli.get_players()
                    elif self.event_status is None:
                        self.event_status = self.cli.get_event_status()
                    else:
                        event_id = self.store.create_event(self.event_name,
                                                           datetime.now() + timedelta(
                                                               minutes=random.randint(5, 15)),
                                                           self.event_participants,
                                                           not self.event_status,
                                                           self.event_location)
                        self.cli.dis_event_info(self.store.get_event(event_id))
                        self.clear_input_buffer()
                        self.con_state = ConState.DISPLAY
                elif self.con_state is ConState.SS_EVENT:
                    if self.event_id == "":
                        self.event_id = self.cli.get_event_id()
                    elif self.player == "":
                        self.player = self.cli.get_player_name()
                    else:
                        try:
                            ss = self.store.get_player_secret_santa(self.event_id, self.player)
                            self.cli.dis_ss_message(self.event_id, self.player, ss)
                        except EventNotFoundException as err:
                            self.cli.dis_error(err.msg)
                        except PlayerNotFoundException as err:
                            self.cli.dis_error(err.msg)
                        self.clear_input_buffer()
                        self.con_state = ConState.DISPLAY

                elif self.con_state is ConState.DISPLAY:
                    res = self.cli.get_global_choice()
                    self.con_state = self.validate_global(res)

                elif self.con_state is ConState.QUIT:
                    self.cli.clear_screen()
                    raise QuitException("Terminate the program")
                else:
                    self.con_state = ConState.MAIN

            except QuitException:
                self.cli.clear_screen()
                exit()



class SSCli:
    """SS cli implementation"""
    def __init__(self):
        self.name = self.__class__.__name__

    def invalid_input_msg(self):
        """prints the message to user for invalid input."""
        print("\nInput that was entered is invalid.")

    def clear_screen(self):
        """clears the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def dis_header_message(self):
        """Display the application header"""
        print("\t**********************************************")
        print("\t***    Welcome to the Secret Santa App     ***")
        print("\t**********************************************")

    def get_main_choices(self):
        """Prints the main menu and get the choice of the user."""
        # Let users know what they can do.
        print("\n[l] See a list of events")
        print("[n] Create a new event")
        print("[g] Get event info")
        print("[a] Add a player")
        print("[r] Remove a player")
        print("[c] Close an event")
        print("[d] Delete an event")
        print("[s] Get player's SS")
        print("[m] Return to main")
        print("[q] Quit")

        return input("What would you like to do? ")


    def _validate_event_id(self, event_id:str) -> str:
        """validate the event id"""
        if len(event_id) == 0:
            return ""
        return event_id
        
    def get_global_choice(self):
        "get the global choice"
        # Let users know what they can do.
        print("\n[l] See a list of events")
        print("[m] Return to main")
        print("[q] Quit.")

        return input("What would you like to do? ")

    def get_event_id(self):
        """get the event id from the user"""
        return self._validate_event_id(input("What is the event id? "))

    def get_location(self):
        """get the location of the event"""
        return input("What is the location of the event? ")

    def get_players(self) -> List[str]:
        """Get the players playing the game"""
        res = input("What is the names of players(ex: john, robert, tom, ...)? ")
        return res.split(",")

    def get_event_status(self) -> bool:
        """Get the status of the events"""
        res = input("Is the event open to the public [Y/n]? ")
        if res.lower() == "y":
            return True
        else:
            return False

    def get_player_name(self):
        """Get the value of the player name"""
        return input("What is the name of the player you want to add? ")

    def get_event_name(self):
        """Get the value of the new event"""
        return input("What is the name of the new event? ")

    def dis_event_close_msg(self, event_id:str):
        """Display event close message"""
        print(f"\n{event_id=} is closed and cannot be modified")

    def dis_event_info(self, event: Event):
        """Displays event info"""
        print(f"\n{event.event_id=}")
        print(f"{event.event_name=}")
        print(f"{event.event_status.name=}")
        print(f"{event.event_location=}")
        print(f"Event datetime={event.event_date_time.strftime('%d-%b-%Y %I:%M %p')}")
        print(f"{event.event_participants=}")
        print(f"{event.event_santa_map=}")

    def dis_event_not_found(self, event_id: str):
        """Displayed a failed event get"""
        print(f"{event_id=} was not found in the system. Are you sure about the event_id?")

    def dis_cancel_event_msg(self, event_id: str):
        """Message when event is deleted"""
        print(f"\n{event_id=} has been deleted")

    def dis_event_update_msg(self, event_id: str):
        """Message when event is deleted"""
        print(f"\n{event_id=} has been updated")

    def dis_ss_message(self, event_id: str, player:str, ss: str):
        """displays the message for secrete santa"""
        print(f"{player=} in this {event_id=} has {ss=} as their secrete santa ")

    def dis_events(self, events: List[Event]):
        """Prints the list names"""
        columns = ("ID.   ",
        "| Name          ",
        "| State  ",
        )
        print()
        header = "".join(columns)
        print(header)
        for event in events:
            event_str = f"{event.event_id[:5]} | {event.event_name} | {event.event_status.name}"
            print(event_str)

    def dis_error(self, msg: str):
        """display any generic error"""
        print("\n", msg)


class SSDataStore:
    """SS Datastore implementation"""
    def __init__(self):
        """SS datastore"""
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
        
        _id = uuid.uuid4()
        while _id in self.store:
            _id = uuid.uuid4()

        event_state = EventStatus.OPEN
        santa_map = {}
        if close_event:
            santa_map = self.__get_santa_map(participants)
            event_state = EventStatus.CLOSED
        event = Event(str(_id), name, date_time, event_state, participants, santa_map, location)
        self.store[str(_id)] = event
        date_time_float = time.mktime(date_time.timetuple())
        heapq.heappush(self.time_queue, (date_time_float, _id))
        return str(_id)

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





if __name__ == "__main__":
    app = SSApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print()
        exit()
