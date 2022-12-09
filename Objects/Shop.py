import json
from typing import Iterable

from Objects.Item import *
import random
from dataclasses import dataclass
from pathlib import Path


#
# Class: Shop
# Takes in the name, shop_type, city, region, wealth, gold amount, and sell multiplier of a shop
@dataclass
class Shop:
    name: str = ""
    owner: str = ""
    notes: str = ""
    shop_type: str = ""
    city: str = ""
    region: str = ""
    wealth: str = ""
    gold_amount: str = ""
    sell_mult: str = ""
    items: dict = None

    def Serialize(self):
        return vars(self)

    def addItems(self, items: dict):  # adds a list of items, given an item list, to the shop
        for key in items:
            self.items[key] = {"Cost": "", "Amount": "0"}
            if items[key]["Base Region"] == self.region:
                self.items[key]["Cost"] = str((float(items[key]["Value"]) * 1 / float(items[key]["Rarity"])) // 2)
            else:
                self.items[key]["Cost"] = str((float(items[key]["Value"]) * 1 / float(items[key]["Rarity"])))

    def addNewItem(self, item: Item, amount: str, cost: float):  # adds a new item to the shop
        self.items[item.name] = {"Cost": float(cost), "Amount": amount}

    def addItem(self, name: str, amount: float):  # adds a previous item to the shop, increasing the amount
        try:
            temp = int(self.items[name]["Amount"])
        except KeyError:
            print("Item is not in shop, please use 'addNewItem'")
            return
        temp += amount
        self.items[name]["Amount"] = temp

    def updateItemPrice(self, item_name: str, cost: float):  # updates the cost of an item
        self.items[item_name]["Cost"] = cost


#
# Class: ShopManager
# Manages the save data of the list of shops, and loads shops from save data
class ShopManager:
    def __init__(self, filename: str='shops.txt'):
        self.items = ItemManager()
        temp = ""
        self.shop_list = {}
        self.file = "../Resources/save_data/" + filename
        self.Deserialize()


    def addShop(self, name, owner, type, city, region, wealth, items, gold_amount,
                sell_multiplier):  # adds a shop by the input values
        temp = Shop(name, owner, type, city, region, wealth, items, gold_amount, sell_multiplier)
        self.shop_list[name] = temp.Serialize()

    def addShop(self, shop):  # adds a shop if you made a shop already
        name = shop.name
        self.shop_list[name] = shop.Serialize()  # loads the shop to the json string

    def saveShops(self):  # saves all the shops into a json file
        open(Path(self.file), 'w').close()
        file = open(Path(self.file), "r+")
        json.dump(self.shop_list, file, indent=4)
        file.close()

    def getShopRegions(self) -> list:  # returns all the regions that shops have
        regions = []
        for key in self.shop_list:
            if self.shop_list[key]["region"] not in regions:
                regions.append(self.shop_list[key]["Region"])
        return regions

    def getShopTypes(self) -> dict:  # returns all the different types of shops
        types = {}
        temp = []
        for key in self.shop_list:
            if self.shop_list[key]["type"] not in temp:
                temp.append(self.shop_list[key]["type"])
        types.update({'Shop Types': temp})
        return types

    def getShopByRegion(self, region: str) -> dict:
        regional_shops = {}
        for k in self.shop_list:
            if self.shop_list[k]["region"] == region:
                regional_shops.update({k: self.shop_list[k]})
        return regional_shops

    def getShopByType(self, type_shop: str) -> dict:
        type_shops = {}
        for k in self.shop_list:
            if self.shop_list[k]["shop_type"] == type_shop:
                type_shops.update({k: self.shop_list[k]})
        return type_shops

    def getShopByCity(self, city: str) -> dict:
        city_shops = {}
        for k in self.shop_list:
            if self.shop_list[k]["city"] == city:
                # print(k)
                city_shops.update({k: self.shop_list[k]})
        return city_shops

    def getShopByTypeinCity(self, city: str, shop_type) -> dict:
        city_shops = {}
        for k in self.shop_list:
            if self.shop_list[k]["city"] == city:
                # print(k)
                if self.shop_list[k]["shop_list"] == shop_type:
                    city_shops.update({k: self.shop_list[k]})
        return city_shops

    def getItemAmount(self, shop_name: str, item: str) -> int:
        return int(self.shop_list[shop_name]["items"][item]["amount"])

    def removeItem(self, shop_name: str, item: str):
        self.shop_list[shop_name]["items"].pop(item)

    def addNewItem(self, shop_name: str, item_name: str):
        shop = self.shop_list[shop_name]
        new_item = self.items.itemList[item_name]
        cost = float(new_item["base_value"])
        cost /= (float(new_item["rarity"]) * random.uniform(.5, .9))
        if new_item["base_region"] == shop["region"]:
            cost /= 1.2
        cost = max(cost, 5.0)
        self.shop_list[shop_name]["items"].update({item_name: {"cost": cost, "amount": "1"}})

    def increaseShopItemAmount(self, shop_name: str, item_name: str):
        shop = self.shop_list[shop_name]
        amount = int(shop["items"][item_name]["amount"])
        amount += 1
        shop["items"][item_name]["amount"] = amount

    def decreaseShopItemAmount(self, shop_name: str, item):
        amount = int(self.shop_list[shop_name]["items"][item]["amount"])
        amount -= 1
        self.shop_list[shop_name]["items"][item]["amount"] = amount

    def decreaseShopGoldAmount(self, shop_name: str, gold):
        amount = int(float(self.shop_list[shop_name]["gold_amount"]))
        amount -= round(gold)
        if amount < 0:
            amount = 0
        self.shop_list[shop_name]["gold_amount"] = amount

    def increaseShopGoldAmount(self, shop_name: str, gold):
        amount = int(float(self.shop_list[shop_name]["gold_amount"]))
        amount += round(gold)
        if amount < 0:
            amount = 0
        self.shop_list[shop_name]["gold_amount"] = amount

    def getShopByName(self, name: str) -> dict:
        return self.shop_list[name]

    def printShopItems(self, shop: str):
        printed_shop = self.shop_list[shop]
        for k in printed_shop["items"]:
            cost = float(self.shop_list[shop]["items"][k]["cost"]) / 100
            if cost < 1:
                cost *= 10
                if cost > 1:
                    cost = str.format("%.1f" % float(cost)) + " sp"
                else:
                    cost *= 10
                    cost = str(int(cost)) + " cp"
            else:
                cost = str.format("%.2f" % float(cost)) + " gp"
            print("%s : %s, Cost : %s" % (k, str(self.shop_list[shop]["items"][k]["amount"]), cost))

    def printShop(self, shop_name: str):
        shop = self.shop_list[shop_name]
        print("Shop name is: ", shop["name"])
        print("Shop shop_type is: ", shop["shop_type"])
        print("Shop City is: ", shop["city"])
        print("Shop Notes are: ", shop["notes"])
        print()
        print("Shop currently has %s gold" % int(float(shop["gold_amount"]) / 100))
        print()
        print("||||||||||||||||||||||||||||||||||||||||||||||||")
        print("||||||||||||||||||||ITEMS|||||||||||||||||||||||")
        self.printShopItems(shop["name"])

    def Deserialize(self):
        temp = ""
        try:
            with open(self.file,
                      "x") as file:  # sees if the file already exists, if it doesn't create the file
                file.write(temp)
                file.close()
        except FileExistsError:
            try:
                with open(  # if the file does exist then load the file contents to the shop_list
                        Path(self.file)) as file:
                    self.shop_list = json.load(file)
            except json.decoder.JSONDecodeError as e:  # if the file is in incorrect json, then don't load it
                print(e)
                self.shop_list = {}
