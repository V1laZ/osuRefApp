from kivy.uix.popup import Popup
from .. import settings


class JoinLobbyPopup(Popup):
    def joinLobby(self, lobbyID):
        """Join lobby and save lobby ID to global variable"""
        settings.irc.sendall(f"JOIN #mp_{lobbyID}\n".encode())
        settings.lobby = lobbyID