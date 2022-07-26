from kivy.uix.popup import Popup
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from .. import settings

class CreateLobbyPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win_cond_menu = [
            {
                "viewclass": "OneLineListItem",
                "text": "Score",
                "height": dp(48),
                "on_release": lambda x = "Score": self.set_item(x, self.win_cond, self.win_cond_dropdown)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Accuracy",
                "height": dp(48),
                "on_release": lambda x = "Accuracy": self.set_item(x, self.win_cond, self.win_cond_dropdown)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Combo",
                "height": dp(48),
                "on_release": lambda x = "Combo": self.set_item(x, self.win_cond, self.win_cond_dropdown)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Score V2",
                "height": dp(48),
                "on_release": lambda x = "Score V2": self.set_item(x, self.win_cond, self.win_cond_dropdown)
            }      
        ]
        self.win_cond_dropdown = MDDropdownMenu(
            items = self.win_cond_menu,
            width_mult = 2,
            position = "center",
            caller = self.win_cond
        )

        self.slots_menu = [
            {
                "viewclass": "OneLineListItem",
                "text": "2",
                "height": dp(48),
                "on_release": lambda x = "2": self.set_item(x, self.slots, self.slots_dropdown)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "4",
                "height": dp(48),
                "on_release": lambda x = "4": self.set_item(x, self.slots, self.slots_dropdown)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "6",
                "height": dp(48),
                "on_release": lambda x = "6": self.set_item(x, self.slots, self.slots_dropdown)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "8",
                "height": dp(48),
                "on_release": lambda x = "8": self.set_item(x, self.slots, self.slots_dropdown)
            }
        ]
        self.slots_dropdown = MDDropdownMenu(
            items = self.slots_menu,
            width_mult = 1,
            position = "center",
            caller = self.slots
        )

        self.modes_menu = [
            {
                "viewclass": "OneLineListItem",
                "text": "Head-to-Head",
                "height": dp(48),
                "on_release": lambda x = "Head-to-Head": self.set_item(x, self.mode, self.modes_dropdown)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Team VS",
                "height": dp(48),
                "on_release": lambda x = "Team VS": self.set_item(x, self.mode, self.modes_dropdown)
            }
        ]
        self.modes_dropdown = MDDropdownMenu(
            items = self.modes_menu,
            width_mult = 2.2,
            position = "center",
            caller = self.mode
        )
    
    def open_win_cond_dropdown(self):
        self.win_cond_dropdown.open()

    def open_slots_dropdown(self):
        self.slots_dropdown.open()

    def open_modes_dropdown(self):
        self.modes_dropdown.open()

    def set_item(self, item, instance, menu_instance):
        instance.text = item
        menu_instance.dismiss()

    def create_lobby(self):
        """Create mp lobby and save settings to global variables"""

        settings.num_slots = int(self.slots.text)

        if self.win_cond.text == "Score V2":
            settings.win_cond = 3
        elif self.win_cond.text == "Combo":
            settings.win_cond = 2
        elif self.win_cond.text == "Accuracy":
            settings.win_cond = 1
        else:
            settings.win_cond = 0

        if self.mode.text == "Head-to-Head":
            settings.mode = 0
        elif self.mode.text == "Team VS":
            settings.mode = 2

        settings.irc.sendall(f"PRIVMSG banchobot :!mp make {self.prefix.text}: ({self.team1.text}) vs ({self.team2.text})\n".encode())