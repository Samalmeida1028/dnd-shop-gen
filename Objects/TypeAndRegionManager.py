from Objects.Item import *
from Objects.Shop import ShopManager
from Objects.Item import ItemManager


class TypeManager:

    def __init__(self, shop: ShopManager, item: ItemManager, filename="types.txt"):

        self.item_types = item.getItemTypes()  # gets all the item Types
        self.shop_types = shop.getShopTypes()  # gets all the shop Types
        self.filename = filename
        self.type_list = {}
        try:
            with open("../Resources/save_data/"+self.filename, "x") as file:
                file.write("")
                file.close()
        except FileExistsError:
            try:
                with open("../Resources/save_data/"+self.filename) as file:
                    self.type_list = json.load(file)
            except json.decoder.JSONDecodeError as e:
                self.type_list = {}

        for key in self.type_list:
            self.type_list.update({key: self.type_list[key]})
            # updates all the keys with the types in the save file
        for key in self.shop_types:
            if key not in self.type_list:
                self.type_list.update({key: []})  # updates all the keys with the types in the save file

    def addItemType(self, key, value):  # adds an item shop_type to a given shop shop_type
        temp = []
        if self.type_list[key]:
            temp += self.type_list[key]
        if temp.count(value) == 0:
            temp += [value]
        if len(temp) != 0:
            self.type_list.update({key: temp})

    def addNewShopType(self, key):
        if key not in self.type_list:
            self.type_list.update({key: []})

    def removeItemType(self, key, value):  # removes an item shop_type from a given shop shop_type
        temp = []
        if self.type_list[key]:
            temp += self.type_list[key]
        if temp.count(value) != 0:
            temp.pop(value)
        if len(temp) != 0:
            self.type_list.update({key: temp})

    def addNewShopItemType(self, key, value): # adds a new shop shop_type and a new item shop_type to the shop shop_type
        if key not in self.type_list:
            print(key)
            self.type_list.update({key: []})
        self.addItemType(key, value)

    def saveTypes(self):  # saves the types for each shop to the save text file
        file = open("../Resources/save_data/"+self.filename, "r+")
        json.dump(self.type_list, file, indent=2)
        file.close()


class RegionManager:
    def __init__(self, shop: ShopManager, item: ItemManager,filename: str = "regions.txt"):
        self.item_regions = item.getItemRegions()  # gets all the item regions
        self.shop_regions = shop.getShopRegions()  # gets all the shop regions
        self.filename = filename
        self.region_list = {}
        try:
            with open("../Resources/save_data/" + self.filename, "x") as file:
                file.write("")
                file.close()
        except FileExistsError:
            try:
                with open("../Resources/save_data/" + self.filename) as file:
                    self.region_list = json.load(file)
            except json.decoder.JSONDecodeError as e:
                self.region_list = {}

        for key in self.region_list:
            self.region_list.update({key: self.region_list[key]})
            # updates all the keys with the regions in the save file
        for key in self.shop_regions:
            if key not in self.region_list:
                self.region_list.update({key: []})  # updates all the keys with the regions in the save file

    def addItemRegion(self, region, item):  # adds an item region to a given shop region
        temp = []
        if self.region_list[region]:
            temp += self.region_list[region]
        if temp.count(item) == 0:
            temp += [item]
        if len(temp) != 0:
            self.region_list.update({region: temp})
        self.saveRegions()

    def addNewShopRegion(self, key):
        if key not in self.region_list:
            self.region_list.update({key: []})
        self.saveRegions()

    def removeItemRegion(self, key, value):  # removes an item region from a given shop region
        temp = []
        if self.region_list[key]:
            temp += self.region_list[key]
        if temp.count(value) != 0:
            temp.pop(value)
        if len(temp) != 0:
            self.region_list.update({key: temp})
        self.saveRegions()

    def addNewShopItemRegion(self, key, value): # adds a new shop region and a new item region to the shop region
        if key not in self.region_list:
            self.region_list.update({key: []})
        self.addItemRegion(key, value)
        self.saveRegions()

    def saveRegions(self):  # saves the regions for each shop to the save text file
        file = open("../Resources/save_data/" + self.filename, "r+")
        json.dump(self.region_list, file, indent=2)
        file.close()