import json
from Objects.Item import ItemManager
import random

#
# Class: Shop
# Takes in the name, type, city, region, wealth, gold amount, and sell multiplier of a shop
class Shop:
    def __init__(self, name="",owner = "",notes = "", shopType="", city="", region="", wealth="", items={}, goldAmount="", sellMult=""):
        self.name = name
        self.owner = owner
        self.shopType = shopType
        self.notes = notes
        self.city = city
        self.region = region
        self.wealth = wealth
        self.items = {}
        if (type(items) != str):
            self.addItems(items)
        self.goldAmount = goldAmount
        self.sellMult = sellMult

    def __str__(self):  # this puts the shop items in JSON format for saving
        temp = json.dumps(self.items, indent=4)
        return '{"Name":"' + self.name + '","Owner":"'+self.owner+'","Notes":"'+self.notes+'","Type":"' + self.shopType + '","City":"' + self.city + '","Region":"' + self.region + '","Wealth":"' + self.wealth + '","Items":' + temp + ',"GoldAmount":"' + self.goldAmount + '","SellMult":"' + self.sellMult + '"}'

    def str(self):
        return self.__str__()

    def addItems(self, items):  # adds a list of items, given an itemlist, to the shop
        for key in items:
            self.items[key] = {"Cost": "", "Amount": "0"}
            if (items[key]["Base Region"] == self.region):
                self.items[key]["Cost"] = str((float(items[key]["Value"]) * 1 / float(items[key]["Rarity"])) // 2)
            else:
                self.items[key]["Cost"] = str((float(items[key]["Value"]) * 1 / float(items[key]["Rarity"])))

    def addNewItem(self, item, Amount, cost):  # adds a new item to the shop
        self.items[item.name] = {"Cost": float(cost), "Amount": Amount}

    def addItem(self, name, amount):  # adds a previous item to the shop, increasing the amound
        temp = int(self.items[name]["Amount"])
        temp += amount
        self.items[name]["Amount"] = temp

    def updateItemPrice(self, itemName, cost):  # updates the cost of an item
        temp = int(self.items[itemName]["Cost"])
        temp = cost
        self.items[itemName]["Cost"] = temp


#
# Class: ShopManager
# Manages the save data of the list of shops, and loads shops from save data
class ShopManager:
    def __init__(self):
        self.items = ItemManager()
        temp = ""
        self.shopList = {}
        try:
            with open("../Resources/save_data/shops.txt",
                      "x") as file:  # sees if the file already exists, if it doesn't create the file
                file.write(temp)
                file.close()
        except FileExistsError:
            try:
                with open(  # if the file does exist then load the file contents to the shopList
                        "../Resources/save_data/shops.txt") as file:
                    self.shopList = json.load(file)
            except json.decoder.JSONDecodeError as e:  # if the file is in incorrect json, then don't load it
                print(e)
                self.shopList = {}

    def addShop(self, name,owner, type, city, region, wealth, items, goldAmount, sellMult):  # adds a shop by the input values
        temp = Shop(name,owner,type,city, region, wealth, items, goldAmount, sellMult)
        self.shopList[name] = json.loads(temp.str())

    def addShop(self, shop):  # adds a shop if you made a shop already
        name = shop.name
        self.shopList[name] = json.loads(shop.str())  # loads the shop to the json string

    def saveShops(self):  # saves all the shops into a json file
        open('../Resources/save_data/shops.txt', 'w').close()
        file = open("../Resources/save_data/shops.txt", "r+")
        json.dump(self.shopList, file, indent=4)
        file.close()

    def getShopRegions(self):  # returns all the regions that shops have
        regions = []
        for key in self.shopList:
            if self.shopList[key]["Region"] not in regions:
                regions.append(self.shopList[key]["Region"])
        return regions

    def getShopTypes(self):  # returns all the different types of shops
        types = {}
        temp = []
        for key in self.shopList:
            if self.shopList[key]["Type"] not in temp:
                temp.append(self.shopList[key]["Type"])
        types.update({'Shop Types': temp})
        return types

    def getShopByRegion(self, region):
        regionalShops = {}
        for k in self.shopList:
            if self.shopList[k]["Region"] == region:
                # print(k)
                regionalShops.update({k: self.shopList[k]})
        return regionalShops

    def getShopByType(self, type):
        typeShops = {}
        for k in self.shopList:
            if self.shopList[k]["Type"] == type:
                # print(k)
                typeShops.update({k: self.shopList[k]})
        return typeShops

    def getShopByCity(self, city):
        cityShops = {}
        for k in self.shopList:
            if self.shopList[k]["City"] == city:
                # print(k)
                cityShops.update({k: self.shopList[k]})
        return cityShops

    def getShopByTypeinCity(self, city, type):
        cityShops = {}
        for k in self.shopList:
            if self.shopList[k]["City"] == city:
                # print(k)
                if self.shopList[k]["Type"] == type:
                    cityShops.update({k: self.shopList[k]})
        return cityShops

    def getItemAmount(self,shopName,item):
        return int(self.shopList[shopName]["Items"][item]["Amount"])

    def removeItem(self,shopName, item):
        self.shopList[shopName]["Items"].pop(item)

    def addNewItem(self,shopName, itemName):
        shop = self.shopList[shopName]
        newItem = self.items.itemList[itemName]
        cost = float(newItem["Value"])
        cost /= (float(newItem["Rarity"])*random.uniform(.5,.9))
        if(newItem["Base Region"] == shop["Region"]):
            cost /= 1.2
        cost = min(cost,5.0)
        self.shopList[shopName]["Items"].update({itemName: {"Cost": cost, "Amount": "1"}})

    def increaseShopItemAmount(self, shopName, itemName):
        shop = self.shopList[shopName]
        amount = int(shop["Items"][itemName]["Amount"])
        amount += 1
        shop["Items"][itemName]["Amount"] = amount


    def decreaseShopItemAmount(self, shopName, item):
        amount = int(self.shopList[shopName]["Items"][item]["Amount"])
        amount -= 1
        self.shopList[shopName]["Items"][item]["Amount"] = amount

    def decreaseShopGoldAmount(self, shopName, gold):
        amount = int(float(self.shopList[shopName]["GoldAmount"]))
        amount -= round(gold)
        if(amount < 0):
            amount = 0
        self.shopList[shopName]["GoldAmount"] = amount

    def getShopbyName(self, name):
        return self.shopList[name]

    def printShopItems(self,shop):
        printedShop = self.shopList[shop]
        for k in printedShop["Items"]:
            cost = float(self.shopList[shop]["Items"][k]["Cost"])/100
            if(cost < 1):
                cost *= 10
                if(cost > 1):
                    cost = str(int(cost)) + " sp"
                else:
                    cost *= 10
                    cost = str(int(cost)) + " cp"
            else:
                cost = str(int(cost)) + " gp"
            print("%s : %s, Cost : %s" %(k,str(self.shopList[shop]["Items"][k]["Amount"]),cost))

    def printShop(self, shopName):
        shop = self.shopList[shopName]
        print("Shop name is: ", shop["Name"])
        print("Shop type is: ", shop["Type"])
        print()
        print("Shop currently has %s gold" % int(float(shop["GoldAmount"])/100))
        print()
        print("||||||||||||||||||||||||||||||||||||||||||||||||")
        print("||||||||||||||||||||ITEMS|||||||||||||||||||||||")
        self.printShopItems(shop["Name"])
