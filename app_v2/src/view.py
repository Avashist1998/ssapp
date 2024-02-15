import os
from typing import List

from src.models import Event

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
