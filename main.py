import json
import os
import socket
import threading

from kivy.clock import mainthread
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FloatLayout, ScreenManager
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import Screen
from kivymd.uix.menu import MDDropdownMenu

#from extractPool import extractMapPools

Window.size = (280, 570)
Window.softinput_mode = 'below_target'
Config.set('kivy', 'exit_on_escape', '0')

class LoginWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        try:
            with open('login.json') as f:
                data = json.load(f)
                self.username_text = data["osu_IRC_name"]
                self.password_text = data["osu_IRC_token"]
        except FileNotFoundError:
            with open('login.json', 'w') as f:
                data = {"osu_IRC_name": "", "osu_IRC_token": ""}
                json.dump(data, f)
                self.username_text = data["osu_IRC_name"]
                self.password_text = data["osu_IRC_token"]


    def login(self, username, password):
        """Login to Bancho IRC and start listener"""
        irc.connect((SERVER, PORT))
        irc.sendall(f"PASS {password}\n".encode())
        irc.sendall(f"USER {username}\n".encode())
        irc.sendall(f"NICK {username}\n".encode())
        data = irc.recv(2048).decode()
        if "001" in data:
            global nick
            nick = username
            self.errorMsg.text = ""
            print("Connected to Bancho")
            MDApp.get_running_app().root.ids.main_window.listener()
            return True
        elif "464" in data:
            irc.close()
            self.errorMsg.text = "Bad authentication token."
            create_socket()
            print("Couldn't connect to Bancho")
            return False

    def remember(self, name, password):
        """Save name and password to login.json"""
        with open('login.json', "r") as f:
            data = json.load(f)
            data["osu_IRC_name"] = name
            data["osu_IRC_token"] = password
        
        with open('login.json', "w") as f:
            json.dump(data, f, indent=2)

    def dont_remember(self):
        """Remove name and password from login.json"""
        with open('login.json', "r") as f:
            data = json.load(f)
            data["osu_IRC_name"] = ""
            data["osu_IRC_token"] = ""
        
        with open('login.json', "w") as f:
            json.dump(data, f, indent=2)

class LobbyInitWindow(Screen):
    pass

class JoinLobbyPopup(Popup):
    def joinLobby(self, lobbyID):
        """Join lobby and save lobby ID to global variable"""
        irc.sendall(f"JOIN #mp_{lobbyID}\n".encode())
        global lobby
        lobby = lobbyID

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
        global win_cond
        global num_slots
        global mode

        num_slots = int(self.slots.text)

        if self.win_cond.text == "Score V2":
            win_cond = 3
        elif self.win_cond.text == "Combo":
            win_cond = 2
        elif self.win_cond.text == "Accuracy":
            win_cond = 1
        else:
            win_cond = 0

        if self.mode.text == "Head-to-Head":
            mode = 0
        elif self.mode.text == "Team VS":
            mode = 2

        irc.sendall(f"PRIVMSG banchobot :!mp make {self.prefix.text}: ({self.team1.text}) vs ({self.team2.text})\n".encode())

class MappoolAddPopup(Popup):
    pass

class MappoolInitWindow(Screen):
    pass

class MappoolAddWindow(Screen):
    pass

class MappoolSavePopup(Popup):
    def write_mappool(self, mappool, name):
        """Create json file with mappool info and append new row to mappool table"""
        with open(f"mappools/{name}.json", "w") as fp:
            json.dump(mappool, fp)
            print(f"Write {name}")

        MDApp.get_running_app().mappool_table.row_data.append((name, ""))
        MDApp.get_running_app().mappool_table.update_row_data(MDApp.get_running_app().mappool_table, MDApp.get_running_app().mappool_table.row_data)

class MappoolRemovePopup(Popup):
    def removeMappool(self, name: str):
        """Remove json file with mappool info and remove corresponding row from mappool table"""
        try:
            os.remove(f"mappools/{name}.json")
        except FileNotFoundError:
            print("File not found")
            return

        MDApp.get_running_app().mappool_table.row_data.remove((name, ""))
        MDApp.get_running_app().mappool_table.update_row_data(MDApp.get_running_app().mappool_table, MDApp.get_running_app().mappool_table.row_data)

class CreateMappoolWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.createMappoolTable = None
    
    def add_table(self):
        """Initialize and add table widget to this screen"""
        if self.createMappoolTable != None:
            return

        self.createMappoolTable = MDDataTable(
            rows_num = 20,
            pos_hint = {"center_x": 0.5, "top": 0.9},
            size_hint = (0.8, 0.6),
            column_data=[
                ("Type", dp(17)),
                ("Map ID", dp(17)),
            ],
            row_data = []
        )

        self.ids.floatlayout.add_widget(self.createMappoolTable)
    
    def add_row(self, mapType: str, mapID: str):
        """Add new row to initialized table widget on this screen"""
        if mapID.isnumeric() == False:
            if "osu.ppy.sh/beatmapsets" in mapID:
                link_split = mapID.split("/")
                mapID = link_split[-1]
            elif "old.ppy.sh/b" in mapID:
                link_split = mapID.split("/")
                mapID = link_split[-1]
            else:
                return

        nextMap = ""
        num = ""
        for i in mapType:
            if i.isnumeric():
                num += i
            else:
                nextMap += i
        
        if num != "":
            num = int(num) + 1
        nextMap = f"{nextMap}{num}"
        self.mapType.text = nextMap

        self.createMappoolTable.row_data.append([mapType.upper(), mapID])
        self.createMappoolTable.rows_num += 1


class SelectMappoolWindow(Screen):
    pass


class MainWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mappoolPopup = ModalView(
            size_hint = (0.8, 0.8),
            pos_hint = {"center_x": 0.5, "center_y": 0.5}
        )
        self.mappoolTable = None

    def sendChatInput(self, text: str):
        """Send text to mp lobby chat and add it to chat widget"""
        irc.sendall(f"PRIVMSG #mp_{lobby} :{text}\n".encode())
        self.addChatMsg(f"{nick}: {text}")

    @mainthread
    def addChatMsg(self, text: str):
        self.chat.text += f"{text}\n"

    @mainthread
    def init_players(self, players: list):
        self.players.text = ""
        for player in players:
            self.players.text += f"{player}\n"

    @mainthread
    def update_players(self, playerSlots: dict):
        slots = ""
        for key, player in playerSlots.items():
            slots += f"{key} {player}\n"
        
        self.players.text = slots[:-1]
    
    @mainthread
    def update_map(self, mapID = None, mapName = None):
        self.beatmap.text = mapName

    def openMappool(self):
        """Open mappool popup for selecting next map"""
        self.mappoolPopup.open()
    
    def mappool_row_pressed(self, instance_table, instance_row):
        """Called when row is pressed in mappool popup window. Sets pressed map in mp lobby"""
        text = instance_row.text
        row_data = instance_table.row_data
        try:
            int(text)
            self.selectMap(text)
            self.mappoolPopup.dismiss()
        except:
            for i in row_data:
                if text in i:
                    self.selectMap(i[1])
                    self.mappoolPopup.dismiss()
    
    def selectMap(self, mapID):
        self.sendChatInput(f"!mp map {mapID}")


    def listener(self, running=False):
        """Listen for incoming data from Bancho and do things"""
        if not running:
            threading.Thread(target=self.listener, args=(True,)).start()
        else:
            started = True
            print("Started listening")
            buffer = ""
            players = []
            playerSlots = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: ""}
            data = ""

            while started:
                while True:
                    part = irc.recv(1024).decode()
                    data += part
                    if len(part) != 1024:
                        break
                buffer = data.split("\n")
                for i in buffer:
                    msg = i.replace("!cho@ppy.sh", "")
                    if "QUIT" in msg or msg == "":
                        continue
                    elif "PING" in msg:
                        irc.sendall(f"{msg.replace('PING', 'PONG')}\n".encode())
                        print("Received PING sent PONG")
                    elif "353" in msg:
                        print(msg)
                        players = i.split(" ")
                        players = players[6:]
                        players.pop()
                        for player in players:
                            if player[0] == "+":
                                players.remove(player)
                        self.init_players(players)
                    elif "PRIVMSG" in msg:
                        privmsg = msg.split(" ")
                        if privmsg[0] == ":BanchoBot" and privmsg[3] == ":Created":
                            print(msg)
                            link_split = privmsg[7].split('/')
                            lobbyID = link_split[-1]
                            global lobby
                            lobby = lobbyID
                            self.sendChatInput(f"!mp set {mode} {win_cond} {num_slots}")
                        elif privmsg[0] != ":BanchoBot" and privmsg[2][:3] == "#mp":
                            privmsg[3] = privmsg[3].replace(":", "")
                            user = privmsg[0].replace(":", "")
                            message = privmsg[3:]
                            self.addChatMsg(f"{user}: {' '.join(message)}")
                        elif privmsg[0] == ":BanchoBot" and privmsg[2][:3] == "#mp":
                            privmsg = privmsg[3:]
                            if ":Room" in privmsg:
                                privmsg = privmsg[2:]
                                roomName = privmsg[:privmsg.index("History:")]
                                roomName = " ".join(roomName)
                                roomName = roomName[:-1]
                                self.roomName.text = roomName
                            elif ":Beatmap:" in privmsg:
                                beatmapName = privmsg[2:]
                                beatmapName = " ".join(beatmapName)
                                self.update_map(mapName=beatmapName)
                            elif ":Players:" in privmsg:
                                players_num = int(privmsg[1])
                            elif ":Slot" in privmsg:
                                slot_num = int(privmsg[1])
                                if privmsg[3] == "Not":
                                    slot_status = "Not Ready"
                                else:
                                    slot_status = "Ready"
                                for i in privmsg:
                                    if "osu.ppy.sh" in i:
                                        slot_player = privmsg[privmsg.index(i)+1]
                                        break
                                player_info = f"{slot_player} ({slot_status})"
                                if slot_num <= 8:
                                    for key, value in playerSlots.items():
                                        if player_info == value:
                                            playerSlots[key] = ""
                                            break
                                    playerSlots[slot_num] = player_info
                                self.update_players(playerSlots)
                            elif ":Changed" in privmsg:
                                if "settings" in privmsg[2]:
                                    pass
                                else:
                                    self.update_map(mapName=" ".join(privmsg[4:]))
                            elif "moved" in privmsg:
                                moving_player = privmsg[0][1:]
                                moving_to = int(privmsg[-1])
                                for key, value in playerSlots.items():
                                    if moving_player in value:
                                        moving_from = key
                                        playerSlots[moving_from] = ""
                                        break
    
                                playerSlots[moving_to] = moving_player
                                if moving_to <= 8:
                                    playerSlots[moving_to] = moving_player
                                    self.update_players(playerSlots)
                            elif "changed" in privmsg:
                                self.update_map(mapName=" ".join(privmsg[3:-1]))
                            else:
                                chatmsg = " ".join(privmsg)
                                print(f"BanchoBot {chatmsg}")
                                self.addChatMsg(f"BanchoBot {chatmsg}")

                    else:
                        print(msg)
                data = ""


class WindowManager(ScreenManager):
    pass
    


SERVER = "irc.ppy.sh"
PORT = 6667
nick = ""

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def create_socket():
    """Reinitialize socket"""
    global irc
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lobby = ""
win_cond = 0
num_slots = 0
mode = 0


class MyMainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mappoolTableGS = None
        self.mappool_table = None
        self.selectedMappool = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Pink"
        kv = Builder.load_file("style.kv")
        return kv

    # def add_mappoolTableGS(self, link, listName):
    #     """Initialize table widget with extracted mappool from Google Sheets and add it to mappoolAdd screen"""
    #     mappool = extractMapPools(link, listName)

    #     self.mappoolTableGS = MDDataTable(
    #         rows_num = len(mappool[0]),
    #         size_hint = (0.7, 0.7),
    #         pos_hint= {"center_x": 0.5, "top": 0.95},
    #         column_data=[
    #             ("Type", dp(15)),
    #             ("Map ID", dp(15)),
    #         ],
    #         row_data=[
                
    #         ]
    #     )

    #     for i in mappool[0]:
    #         print(i)
    #         self.mappoolTableGS.row_data.append(i)

    #     self.mappoolTableGS.bind(on_row_press=self.mappoolTableGS_row_pressed)
    #     self.root.ids.mappool_add.ids.floatlayout.add_widget(self.mappoolTableGS)

    def mappoolTableGS_row_pressed(self, instance_table, instance_row):
        popup = Popup(
            title = "Change value",
            size_hint = (0.8, 0.3)
        )

        layout = FloatLayout()

        textinput = TextInput(
            text = instance_row.text,
            pos_hint = {"top": 0.85, "center_x": 0.5},
            size_hint = (0.8, 0.27),
            halign = "center"
        )

        btn = Button(
            text = "Save",
            pos_hint = {"center_x": 0.5, "top": 0.38},
            size_hint =  (0.26, 0.27),
            on_release = lambda x: self.mappoolTableGS_save_pressed(textinput.text, popup, instance_row, instance_table)
        )

        layout.add_widget(textinput)
        layout.add_widget(btn)
        popup.add_widget(layout)
        popup.open()

    def mappoolTableGS_save_pressed(self, text, popup_instance, instance_row, instance_table):
        for map in instance_table.row_data:
            for value in map:
                if value == instance_row.text:
                    self.mappoolTableGS.row_data[instance_table.row_data.index(map)][map.index(value)] = text
        self.mappoolTableGS.update_row_data(self.mappoolTableGS, self.mappoolTableGS.row_data)
        popup_instance.dismiss()

    def addMappoolTable(self):
        """Initialize mappool table widget and add it to mappoolInit screen"""
        if os.path.exists("mappools/") is False:
            os.mkdir("mappools/")
        json_files = os.listdir("mappools/")
        file_names = []

        for file in json_files:
            file_names.append(file.replace(".json", ""))

        self.mappool_table = MDDataTable(
            rows_num = 10,
            size_hint = (0.7, 0.53),
            pos_hint = {"center_x": 0.5, "top": 0.63},
            column_data = [
                ("Name", dp(30)),
                ("", dp(1))
            ],
            row_data = [

            ]
        )

        for name in file_names:
            self.mappool_table.row_data.append((name, ""))
        
        self.mappool_table.bind(on_row_press=self.mappool_row_pressed)
        self.root.ids.mappool_init.ids.floatlayout.add_widget(self.mappool_table)

    def mappool_row_pressed(self, instance_table, instance_row):
        """Called when row is pressed in mappool_table widget. Initialize and show new window with corresponding mappool"""
        mappool_name = instance_row.text

        with open(f"mappools/{mappool_name}.json") as f:
            data = json.load(f)

        mappool_popup = ModalView(
            size_hint = (0.8, 0.8),
            pos_hint = {"center_x": 0.5, "center_y": 0.5}
        )

        mappool = MDDataTable(
            rows_num = len(data),
            pos_hint = {"center_x": 0.5, "top": 1},
            column_data=[
                ("Type", dp(17)),
                ("Map ID", dp(17)),
            ],
            row_data = data
        )

        mappool_popup.add_widget(mappool)
        mappool_popup.open()

    def addSelectMappoolTable(self):
        """Initialize mappool table widget and add it to selectMappool screen"""
        if os.path.exists("mappools/") is False:
            os.mkdir("mappools/")
        json_files = os.listdir("mappools/")
        file_names = []

        for file in json_files:
            file_names.append(file.replace(".json", ""))

        self.mappool_table = MDDataTable(
            rows_num = 10,
            size_hint = (0.7, 0.7),
            pos_hint = {"center_x": 0.5, "top": 0.8},
            column_data = [
                ("Name", dp(30)),
                ("", dp(1))
            ],
            row_data = [

            ]
        )

        for name in file_names:
            self.mappool_table.row_data.append((name, ""))
        
        self.mappool_table.bind(on_row_press=self.selectMappool_row_pressed)
        self.root.ids.select_mappool.ids.floatlayout.add_widget(self.mappool_table)

    def selectMappool_row_pressed(self, instance_table, instance_row):
        mappool_name = instance_row.text
        with open(f"mappools/{mappool_name}.json") as f:
            data = json.load(f)

        mappool = MDDataTable(
            rows_num = len(data),
            column_data=[
                ("Type", dp(17)),
                ("Map ID", dp(17)),
            ],
            row_data = data
        )

        mappool.bind(on_row_press=MDApp.get_running_app().root.ids.main_window.mappool_row_pressed)
        MDApp.get_running_app().root.ids.main_window.mappoolPopup.add_widget(mappool)

        self.root.current = "main"


if __name__ == "__main__":
    MyMainApp().run()
