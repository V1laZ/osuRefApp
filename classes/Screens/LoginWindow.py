import json
import socket

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from .. import settings

def create_socket():
    """Reinitialize socket"""
    settings.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class LoginWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        try:
            with open('login.json', "r") as f:
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
        settings.irc.connect((settings.SERVER, settings.PORT))
        settings.irc.sendall(f"PASS {password}\n".encode())
        settings.irc.sendall(f"USER {username}\n".encode())
        settings.irc.sendall(f"NICK {username}\n".encode())
        data = settings.irc.recv(2048).decode()
        if "001" in data:
            settings.nick = username
            print(settings.nick)
            self.errorMsg.text = ""
            print("Connected to Bancho")
            MDApp.get_running_app().root.ids.main_window.listener()
            return True
        elif "464" in data:
            settings.irc.close()
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
