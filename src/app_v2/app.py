"""Version 2 of the Secret Santa application"""
import random
from datetime import datetime, timedelta

from models import ConState
from view import SSCli
from store import SSDataStore
from exceptions import EventNotFoundException, PlayerNotFoundException, QuitException

class SSApp:
    """Secrete Santa Application"""

    def __init__(self):
        self.con_state = ConState.MAIN
        self.cli = SSCli()
        self.store = SSDataStore()

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

