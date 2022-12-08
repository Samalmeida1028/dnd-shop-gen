import json


class Item:

    def __init__(self, name, baseRegion, item_type="misc", baseValue="1", rarity="1", arg=[]):
        if len(arg) == 0:
            self.name = name
            self.item_type = item_type
            self.baseValue = baseValue
            self.rarity = rarity
            self.baseRegion = baseRegion
        else:
            self.name = arg[0]
            self.item_type = arg[1]
            self.baseValue = arg[2]
            self.rarity = arg[3]
            self.baseRegion = arg[4]

    def __str__(self):
        return '{"Name":"' + self.name + '","Type":"' + self.item_type + '","Value":"' + self.baseValue + '","Rarity":"'\
               + self.rarity + '","Base Region":"' + self.baseRegion + '"}'

    def str(self):
        return self.__str__()


class ItemManager:

    def __init__(self):  # inits by trying to load an items.txt json for the save data, else it creates a new one
        temp = ""
        self.item_types = []
        self.itemRegions = []
        self.itemList = {}
        try:
            with open("../Resources/save_data/items.txt", "x") as file:
                file.write(temp)
                file.close()
        except FileExistsError:
            try:
                with open("../Resources/save_data/items.txt") as file:  # loads the json file into a dictionary
                    self.itemList = json.load(file)
            except json.decoder.JSONDecodeError:
                self.itemList = {}

    def addItem(self, name, item_type, baseValue, rarity, baseRegion):  # add item by property
        temp = Item(name, item_type, baseValue, rarity, baseRegion)
        self.itemList[name] = json.loads(temp.str())

    def addItem(self, item_list):  # add new item by list
        temp = Item("", "", "", "", "", item_list)
        self.itemList[item_list[0]] = json.loads(temp.str())

    def getItemRegions(self) -> list:  # returns a list of all the regions in the item list
        for key in self.itemList:
            if self.itemList[key]["Base Region"] not in self.itemRegions:
                self.itemRegions.append(self.itemList[key]["Base Region"])
        return self.itemRegions

    def getItemTypes(self) -> list:  # gets all the item types in the item list
        for key in self.itemList:
            if self.itemList[key]["Type"] not in self.item_types:
                self.item_types.append(self.itemList[key]["Type"])
        return self.item_types

    def getItemIndex(self, index) -> Item:  # gets the index of an item in the item list
        item_name = list(self.itemList)[int(index)]
        item = Item(item_name, self.itemList[item_name]["Base Region"], self.itemList[item_name]["Type"],
                    self.itemList[item_name]["Value"], self.itemList[item_name]["Rarity"])
        return item

    def getItemName(self, name) -> Item:  # gets an item if given a name
        item = Item(name, self.itemList[name]["Base Region"], self.itemList[name]["Type"], self.itemList[name]["Value"],
                    self.itemList[name]["Rarity"])
        return item

    def saveItems(self):  # saves the items to the txt file
        open('../Resources/save_data/items.txt', 'w').close()
        file = open("../Resources/save_data/items.txt", "r+")
        json.dump(self.itemList, file, indent=4)
        file.close()
