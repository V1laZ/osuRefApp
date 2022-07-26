import json

from kivy.uix.popup import Popup
from kivymd.app import MDApp


class MappoolSavePopup(Popup):
    def write_mappool(self, mappool, name):
        """Create json file with mappool info and append new row to mappool table"""
        with open(f"mappools/{name}.json", "w") as fp:
            json.dump(mappool, fp)
            print(f"Write {name}")

        MDApp.get_running_app().mappool_table.row_data.append((name, ""))
        MDApp.get_running_app().mappool_table.update_row_data(MDApp.get_running_app().mappool_table, MDApp.get_running_app().mappool_table.row_data)
