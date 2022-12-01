from Objects.Item import *


class TypeManager:

    def __init__(self, shop, item):

        self.itemTypes = item.getItemTypes()  # gets all the item Types
        self.shopTypes = shop.getShopTypes()  # gets all the shop Types
        self.typeManager = {}  # this is to manage the save file for the supported item Types for each shop
        try:
            with open("../Resources/save_data/types.txt", "x") as file:
                file.write("")
                file.close()
            self.typeList = {}
        except FileExistsError:
            try:
                with open("../Resources/save_data/types.txt") as file:
                    self.typeList = json.load(file)
            except json.decoder.JSONDecodeError:
                self.typeList = {}
        for key in self.typeList:
            self.typeManager.update({key: self.typeList[key]})  # updates all the keys with the types in the save file

    def addItemType(self, key, value):  # adds an item shop_type to a given shop shop_type
        temp = []
        if self.typeManager[key] != '':
            temp += self.typeManager[key]
        if temp.count(value) == 0:
            temp += [value]
        if len(temp) != 0:
            self.typeManager.update({key: temp})

    def addNewShopType(self, key):
        if key not in self.typeManager:
            self.typeManager.update({key: ""})

    def removeItemType(self, key, value):  # removes an item shop_type from a given shop shop_type
        temp = []
        if self.typeManager[key] != '':
            temp += self.typeManager[key]
        if temp.count(value) != 0:
            temp.pop(value)
        if len(temp) != 0:
            self.typeManager.update({key: temp})

    def addNewShopItemType(self, key, value): # adds a new shop shop_type and a new item shop_type to the shop shop_type
        if key not in self.typeManager:
            print(key)
            self.typeManager.update({key: ""})
        self.addItemType(key, value)

    def saveTypes(self):  # saves the types for each shop to the save text file
        file = open("../Resources/save_data/types.txt", "r+")
        json.dump(self.typeManager, file, indent=4)
        file.close()


class RegionManager:
    def __init__(self, shop, item):
        self.itemRegions = item.getItemRegions()  # gets all the item regions
        self.shopRegions = shop.getShopRegions()  # gets all the shop regions
        self.regionManager = {}  # this is to manage the save file for the supported item regions for each shop
        try:
            with open("../Resources/save_data/regions.txt", "x") as file:
                file.write("")
                file.close()
            self.regionList = {}
        except FileExistsError:
            try:
                with open("../Resources/save_data/regions.txt") as file:
                    self.regionList = json.load(file)
            except json.decoder.JSONDecodeError:
                self.regionList = {}
        for key in self.regionList:
            self.regionManager.update({key: self.regionList[key]})
            # updates all the keys with the regions in the save file
        count = 0
        for key in self.shopRegions:
            if key not in self.regionManager:
                self.regionManager.update({key: '[]'})  # updates all the keys with the regions in the save file
            count += 1

    def addItemRegion(self, key, value):  # adds an item region to a given shop region
        temp = []
        if self.regionManager[key] != '':
            temp += self.regionManager[key]
        if temp.count(value) == 0:
            temp += [value]
        if len(temp) != 0:
            self.regionManager.update({key: temp})

    def addNewShopRegion(self, key):
        if key not in self.regionManager:
            self.regionManager.update({key: "[]"})

    def removeItemRegion(self, key, value):  # removes an item region from a given shop region
        temp = []
        if self.regionManager[key] != '':
            temp += self.regionManager[key]
        if temp.count(value) != 0:
            temp.pop(value)
        if len(temp) != 0:
            self.regionManager.update({key: temp})

    def addNewShopItemRegion(self, key, value): # adds a new shop region and a new item region to the shop region
        if key not in self.regionManager:
            self.regionManager.update({key: ""})
        self.addItemRegion(key, value)

    def saveRegions(self):  # saves the regions for each shop to the save text file
        file = open("../Resources/save_data/regions.txt", "r+")
        json.dump(self.regionManager, file, indent=4)
        file.close()