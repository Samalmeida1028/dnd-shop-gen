import json
from Objects.Item import ItemManager
import random


#
# Class: Shop
# Takes in the name, shop_type, city, region, wealth, gold amount, and sell multiplier of a shop
class Shop:
    def __init__(self, name="", owner="", notes="", shop_type="", city="", region="", wealth="", items={}, gold_amount="",
                 sell_mult=""):
        self.name = name
        self.owner = owner
        self.shopType = shop_type
        self.notes = notes
        self.city = city
        self.region = region
        self.wealth = wealth
        self.items = {}
        if type(items) != str:
            self.addItems(items)
        self.goldAmount = gold_amount
        self.sell_mult = sell_mult

    def __str__(self):  # this puts the shop items in JSON format for saving
        temp = json.dumps(self.items, indent=4)
        return '{"Name":"' + self.name + '","Owner":"' + self.owner + '","Notes":"' + self.notes + '","Type":"' \
               + self.shopType + '","City":"' + self.city + '","Region":"' + self.region + '","Wealth":"' + self.wealth \
               + '","Items":' + temp + ',"GoldAmount":"' + self.goldAmount + '","SellMult":"' + self.sell_mult + '"}'

    def str(self):
        return self.__str__()

    def addItems(self, items: dict):  # adds a list of items, given an item list, to the shop
        for key in items:
            self.items[key] = {"Cost": "", "Amount": "0"}
            if items[key]["Base Region"] == self.region:
                self.items[key]["Cost"] = str((float(items[key]["Value"]) * 1 / float(items[key]["Rarity"])) // 2)
            else:
                self.items[key]["Cost"] = str((float(items[key]["Value"]) * 1 / float(items[key]["Rarity"])))

    def addNewItem(self, item, amount: str, cost: float):  # adds a new item to the shop
        self.items[item.name] = {"Cost": float(cost), "Amount": amount}

    def addItem(self, name: str, amount: float):  # adds a previous item to the shop, increasing the amount
        temp = int(self.items[name]["Amount"])
        temp += amount
        self.items[name]["Amount"] = temp

    def updateItemPrice(self, item_name: str, cost: float):  # updates the cost of an item
        self.items[item_name]["Cost"] = cost


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

    def addShop(self, name, owner, type, city, region, wealth, items, gold_amount,
                sell_multiplier):  # adds a shop by the input values
        temp = Shop(name, owner, type, city, region, wealth, items, gold_amount, sell_multiplier)
        self.shopList[name] = json.loads(temp.str())

    def addShop(self, shop):  # adds a shop if you made a shop already
        name = shop.name
        self.shopList[name] = json.loads(shop.str())  # loads the shop to the json string

    def saveShops(self):  # saves all the shops into a json file
        open('../Resources/save_data/shops.txt', 'w').close()
        file = open("../Resources/save_data/shops.txt", "r+")
        json.dump(self.shopList, file, indent=4)
        file.close()

    def getShopRegions(self) -> list:  # returns all the regions that shops have
        regions = []
        for key in self.shopList:
            if self.shopList[key]["Region"] not in regions:
                regions.append(self.shopList[key]["Region"])
        return regions

    def getShopTypes(self) -> dict:  # returns all the different types of shops
        types = {}
        temp = []
        for key in self.shopList:
            if self.shopList[key]["Type"] not in temp:
                temp.append(self.shopList[key]["Type"])
        types.update({'Shop Types': temp})
        return types

    def getShopByRegion(self, region: str) -> dict:
        regional_shops = {}
        for k in self.shopList:
            if self.shopList[k]["Region"] == region:
                regional_shops.update({k: self.shopList[k]})
        return regional_shops

    def getShopByType(self, type_shop: str) -> dict:
        type_shops = {}
        for k in self.shopList:
            if self.shopList[k]["Type"] == type_shop:
                type_shops.update({k: self.shopList[k]})
        return type_shops

    def getShopByCity(self, city: str) -> dict:
        city_shops = {}
        for k in self.shopList:
            if self.shopList[k]["City"] == city:
                # print(k)
                city_shops.update({k: self.shopList[k]})
        return city_shops

    def getShopByTypeinCity(self, city: str, shop_type) -> dict:
        city_shops = {}
        for k in self.shopList:
            if self.shopList[k]["City"] == city:
                # print(k)
                if self.shopList[k]["Type"] == shop_type:
                    city_shops.update({k: self.shopList[k]})
        return city_shops

    def getItemAmount(self, shop_name: str, item: str) -> int:
        return int(self.shopList[shop_name]["Items"][item]["Amount"])

    def removeItem(self, shop_name:str, item: str):
        self.shopList[shop_name]["Items"].pop(item)

    def addNewItem(self, shop_name: str, item_name: str):
        shop = self.shopList[shop_name]
        new_item = self.items.itemList[item_name]
        cost = float(new_item["Value"])
        cost /= (float(new_item["Rarity"]) * random.uniform(.5, .9))
        if new_item["Base Region"] == shop["Region"]:
            cost /= 1.2
        cost = max(cost, 5.0)
        self.shopList[shop_name]["Items"].update({item_name: {"Cost": cost, "Amount": "1"}})

    def increaseShopItemAmount(self, shop_name: str, item_name: str):
        shop = self.shopList[shop_name]
        amount = int(shop["Items"][item_name]["Amount"])
        amount += 1
        shop["Items"][item_name]["Amount"] = amount

    def decreaseShopItemAmount(self, shop_name: str, item):
        amount = int(self.shopList[shop_name]["Items"][item]["Amount"])
        amount -= 1
        self.shopList[shop_name]["Items"][item]["Amount"] = amount

    def decreaseShopGoldAmount(self, shop_name: str, gold):
        amount = int(float(self.shopList[shop_name]["GoldAmount"]))
        amount -= round(gold)
        if amount < 0:
            amount = 0
        self.shopList[shop_name]["GoldAmount"] = amount

    def increaseShopGoldAmount(self, shop_name: str, gold):
        amount = int(float(self.shopList[shop_name]["GoldAmount"]))
        amount += round(gold)
        if amount < 0:
            amount = 0
        self.shopList[shop_name]["GoldAmount"] = amount

    def getShopByName(self, name: str) -> dict:
        return self.shopList[name]

    def printShopItems(self, shop: str  ):
        printed_shop = self.shopList[shop]
        for k in printed_shop["Items"]:
            cost = float(self.shopList[shop]["Items"][k]["Cost"]) / 100
            if cost < 1:
                cost *= 10
                if cost > 1:
                    cost = str.format("%.1f" % float(cost)) + " sp"
                else:
                    cost *= 10
                    cost = str(int(cost)) + " cp"
            else:
                cost = str.format("%.2f" % float(cost)) + " gp"
            print("%s : %s, Cost : %s" % (k, str(self.shopList[shop]["Items"][k]["Amount"]), cost))

    def printShop(self, shop_name: str):
        shop = self.shopList[shop_name]
        print("Shop name is: ", shop["Name"])
        print("Shop shop_type is: ", shop["Type"])
        print("Shop City is: ", shop["City"])
        print("Shop Notes are: ", shop["Notes"])
        print()
        print("Shop currently has %s gold" % int(float(shop["GoldAmount"]) / 100))
        print()
        print("||||||||||||||||||||||||||||||||||||||||||||||||")
        print("||||||||||||||||||||ITEMS|||||||||||||||||||||||")
        self.printShopItems(shop["Name"])
