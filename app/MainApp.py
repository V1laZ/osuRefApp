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
