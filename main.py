from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from app.MainApp import MyMainApp
from classes.Popups.CreateLobbyPopup import CreateLobbyPopup
from classes.Popups.JoinLobbyPopup import JoinLobbyPopup
from classes.Popups.MappoolAddPopup import MappoolAddPopup
from classes.Popups.MappoolRemovePopup import MappoolRemovePopup
from classes.Popups.MappoolSavePopup import MappoolSavePopup
from classes.Screens.CreateMappoolWindow import CreateMappoolWindow
from classes.Screens.LobbyInitWindow import LobbyInitWindow
from classes.Screens.LoginWindow import LoginWindow
from classes.Screens.MainWindow import MainWindow
from classes.Screens.MappoolInitWindow import MappoolInitWindow
from classes.Screens.SelectMappoolWindow import SelectMappoolWindow

Window.size = (400, 800)
Window.softinput_mode = 'below_target'
Config.set('kivy', 'exit_on_escape', '0')

LoginWindow

JoinLobbyPopup

MappoolRemovePopup

LobbyInitWindow

MappoolAddPopup

MappoolInitWindow

MappoolSavePopup

CreateMappoolWindow

CreateLobbyPopup

SelectMappoolWindow

MainWindow


class WindowManager(ScreenManager):
    pass
    

if __name__ == "__main__":
    MyMainApp().run()
