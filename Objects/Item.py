import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Item:
    name: str
    item_type: str
    base_value: str
    rarity: float | str
    base_region: str

    def Serialize(self):
        return vars(self)


class ItemManager:

    def __init__(self, filename: str = "items.txt"):  # inits by trying to load an items.txt json for the save data,
        # else it creates a new one
        self.item_types = []
        self.itemRegions = []
        self.item_list = {}
        self.file = "../Resources/save_data/" + filename
        self.Deserialize()

    def addItem(self, name, item_type, base_value, rarity, base_region):  # add item by property
        temp = Item(name, item_type, base_value, rarity, base_region)
        self.item_list[name] = temp.Serialize()
    def getItemRegions(self) -> list:  # returns a list of all the regions in the item list
        for key in self.item_list:
            if self.item_list[key]["base_region"] not in self.itemRegions:
                self.itemRegions.append(self.item_list[key]["base_region"])
        return self.itemRegions

    def getItemTypes(self) -> list:  # gets all the item types in the item list
        for key in self.item_list:
            if self.item_list[key]["item_type"] not in self.item_types:
                self.item_types.append(self.item_list[key]["item_type"])
        return self.item_types

    def getItemIndex(self, index: int | str) -> Item:  # gets the index of an item in the item list
        item_name = list(self.item_list)[int(index)]
        item = Item(item_name, self.item_list[item_name]["item_type"], self.item_list[item_name]["base_value"],
                    self.item_list[item_name]["rarity"], self.item_list[item_name]["base_region"])
        return item

    def getItemName(self, name: str) -> Item:  # gets an item if given a name
        item = Item(name, self.item_list[name]["item_type"], self.item_list[name]["base_value"],
                    self.item_list[name]["rarity"], self.item_list[name]["base_region"])
        return item

    def saveItems(self):  # saves the items to the txt file
        open(Path(self.file), 'w').close()
        file = open(Path(self.file), "r+")
        json.dump(self.item_list, file, indent=4)
        file.close()

    def Deserialize(self):
        temp = ""
        try:
            with open(Path(self.file), "x") as file:
                file.write(temp)
                file.close()
        except FileExistsError:
            try:
                with open(Path(self.file)) as file:  # loads the json file into a dictionary
                    self.item_list = json.load(file)
            except json.decoder.JSONDecodeError:
                self.item_list = {}


