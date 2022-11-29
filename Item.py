import json

class Item:

    def __init__(self, name,  baseRegion, itemType = "misc", baseValue = "1", rarity = "1", arg = []):
        if(len(arg) == 0):
            self.name = name
            self.itemType = itemType
            self.baseValue = baseValue
            self.rarity = rarity
            self.baseRegion = baseRegion
        else:
            self.name = arg[0]
            self.itemType = arg[1]
            self.baseValue = arg[2]
            self.rarity = arg[3]
            self.baseRegion = arg[4]



    def __str__(self):
        return '{"Name":"' + self.name + '","Type":"' + self.itemType + '","Value":"' + self.baseValue + '","Rarity":"' + self.rarity + '","Base Region":"' + self.baseRegion + '"}'
    def str(self):
        return self.__str__()

class ItemManager:

    def __init__(self): #inits by trying to load a items.txt json for the save data, else it creates a new one
        temp = ""
        self.itemTypes = []
        self.itemRegions = []
        self.itemList = {}
        try:
            with open("Resources/save_data/items.txt", "x") as file:
                file.write(temp)
                file.close()
        except FileExistsError:
            try:
                with open("Resources/save_data/items.txt") as file: # loads the json file into a dictionary
                    self.itemList = json.load(file)
            except json.decoder.JSONDecodeError:
                self.itemList = {}

    def addItem(self, name, itemType, baseValue, rarity, baseRegion): #add item by property
        temp = Item(name, itemType, baseValue, rarity, baseRegion)
        self.itemList[name] = json.loads(temp.str())

    def addItem(self, arrlist): ##add new item by list
        temp = Item("","","","","",arrlist)
        self.itemList[arrlist[0]] = json.loads(temp.str())

    def getItemRegions(self): #returns a list of all the regions in the item list
        for key in self.itemList:
            if self.itemList[key]["Base Region"] not in self.itemRegions:
                self.itemRegions.append(self.itemList[key]["Base Region"])
        return self.itemRegions

    def getItemTypes(self): #gets all the item types in the item list
        for key in self.itemList:
            if self.itemList[key]["Type"] not in self.itemTypes:
                self.itemTypes.append(self.itemList[key]["Type"])
        return self.itemTypes

    def getItemIndex(self, index): #gets the index of an item in the item list
        itemName = list(self.itemList)[int(index)]
        item = Item(itemName, self.itemList[itemName]["Base Region"], self.itemList[itemName]["Type"], self.itemList[itemName]["Value"], self.itemList[itemName]["Rarity"])
        return item;

    def getItemName(self,name): #gets an item if given a name
        print(name)
        item = Item(name, self.itemList[name]["Base Region"], self.itemList[name]["Type"], self.itemList[name]["Value"], self.itemList[name]["Rarity"])
        return item

    def saveItems(self): # saves the items to the txt file
        open('Resources/save_data/items.txt', 'w').close()
        file = open("Resources/save_data/items.txt", "r+")
        json.dump(self.itemList, file, indent=4)
        file.close()
