from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

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