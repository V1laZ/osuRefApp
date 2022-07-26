import os

from kivy.uix.popup import Popup
from kivymd.app import MDApp


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