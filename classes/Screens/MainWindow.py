import threading

import classes.settings as settings
from kivy.clock import mainthread
from kivymd.uix.screen import Screen
from kivy.uix.modalview import ModalView


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
        settings.irc.sendall(f"PRIVMSG #mp_{settings.lobby} :{text}\n".encode())
        self.addChatMsg(f"{settings.nick}: {text}")

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
                    part = settings.irc.recv(1024).decode()
                    data += part
                    if len(part) != 1024:
                        break
                buffer = data.split("\n")
                for i in buffer:
                    msg = i.replace("!cho@ppy.sh", "")
                    if "QUIT" in msg or msg == "":
                        continue
                    elif "PING" in msg:
                        settings.irc.sendall(f"{msg.replace('PING', 'PONG')}\n".encode())
                        print("Received PING sent PONG")
                    elif "353" in msg:
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
                            link_split = privmsg[7].split('/')
                            lobbyID = link_split[-1]
                            settings.lobby = lobbyID
                            self.sendChatInput(f"!mp set {settings.mode} {settings.win_cond} {settings.num_slots}")
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
                                self.addChatMsg(f"BanchoBot {chatmsg}")

                    else:
                        print(msg)
                data = ""
