import json
import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FloatLayout
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable


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
            size_hint = (0.7, 0.6),
            pos_hint = {"center_x": 0.5, "top": 0.92},
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
        self.root.ids.mappool_init.ids.floatlayout.add_widget(self.mappool_table, index=3)

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
