from Shop import *
from TypeAndRegionManager import *
import string
shops = ShopManager()
items = ItemManager()
types = TypeManager(shops,items)
regions = RegionManager(shops,items)

printShop = ['print', 'show']
printShopList = ['all', 'shops']
enterShop = ['enter', 'visit', 'e', 'v']
buyItem = ['-', 'buy']
sellItem = ['+', 'sell']
exitArea = ['exit', 'leave']
regionCommand = ["regions"]
addCommand = ["add","+"]
regionManager =["edit regions", "manage regions"]


def main():
    inp = ""
    while inp not in exitArea:
        inp = input(">> ")
        argv = splitInput(inp)
        if inp not in exitArea:
            runCommands(argv)


def splitInput(inp):
    argv = inp.split(",")
    return argv


def runCommands(argv):
    if argv[0] in printShopList:
        pass
    elif argv[0] in printShop:
        pass
    elif argv[0] in enterShop:
        currentShop(argv[1])
    elif argv[0] in regionCommand:
        getAllRegions()
    elif argv[0] in regionManager:
        manageRegions()
    elif argv[0] in addCommand:
        if argv[1] == "shop":
            print("Enter shop fields separated by a comma ([name],[type],[city],[region],[wealth],[items],[gold amount],[sell multiplier]")
            print("Individual items should be separated by a ;")
            shopIn = input(": ")
            args = shopIn.split(",")
            if(len(args) == 8):
                makeShop(args)
            else:
                print("invalid syntax for adding shop")
    else:
        print("command does not exist")

def buyShopItem(arg, name):
    try:
        shops.getItemAmount(name,arg[0])
    except KeyError:
        print("Item not in shop")
        return
    if len(arg) == 1:
        shops.decreaseShopItemAmount(name, arg[0])
        if shops.getItemAmount(name,arg[0]) == 0:
            shops.removeItem(name, arg[0])
        print("Bought 1 %s" % arg[0])
    elif len(arg) == 2:
        itemAmount = int(shops.getItemAmount(name, arg[0]))
        amount = 0
        while(amount < int(arg[1]) and amount<itemAmount):
            shops.decreaseShopItemAmount(name, arg[0])
            if shops.getItemAmount(name, arg[0]) == 0:
                shops.removeItem(name, arg[0])
            amount += 1
        print("Bought %s %s" % (amount, arg[0]))
    shops.saveShops()

def sellShopItem(arg,name):
    shop = shops.shopList[name]
    goldAmount = int(shop["GoldAmount"])
    try:
        item = items.getItemName(arg[0])
        print(item)
    except KeyError:
        print("Item does not exist")
        return
    itemValue = int(item.baseValue)*float(shop["SellMult"])
    if(item.itemType not in types.typeManager[shop["Type"]]):
        itemValue /= 2
    if(item.baseRegion not in regions.regionManager[shop["Region"]]):
        itemValue *= 1.2
    if(arg[0] in shop["Items"]):
        if len(arg) == 1:
            shops.increaseShopItemAmount(name, arg[0])
            shops.decreaseShopGoldAmount(name, itemValue)
            print("Sold 1 %s for %s" %(arg[0],itemValue))
        elif len(arg) == 2:
            amount = 0
            while(amount < int(arg[1]) and itemValue < goldAmount):
                shops.increaseShopItemAmount(name, arg[0])
                shops.decreaseShopGoldAmount(name, itemValue)
                goldAmount -= itemValue
                amount += 1
            print("Sold %s %s(s) for %s" % (amount, arg[0], itemValue*amount))
        else:
            print("Invalid command structure.")
    else:
        if len(arg) == 1:
            shops.addNewItem(name, item.name)
            shops.decreaseShopGoldAmount(name, itemValue)
            print("Sold 1 %s for %s" %(arg[0],itemValue))
        elif len(arg) == 2:
            shops.addNewItem(name, item.name)
            amount = 1
            while(amount < int(arg[1]) and goldAmount > 0):
                shops.increaseShopItemAmount(name, arg[0])
                shops.decreaseShopGoldAmount(name, itemValue)
                goldAmount -= itemValue
                amount += 1
            print("Sold %s %s(s) for %s" % (amount, arg[0], itemValue*amount))

def runShopCommands(arg, name):
    if arg[0] in buyItem:
        try:
            buyShopItem(arg[1:], name)
        except KeyError:
            print("Item is not in shop")
    elif arg[0] in sellItem:
        sellShopItem(arg[1:], name)
    elif arg[0] in printShop:
        shops.printShop(name)
    else:
        print("command not found")



def currentShop(name):
    name = string.capwords(name.strip())
    cur = ""
    try:
        shops.printShop(name)
    except KeyError:
        print("Shop does not exist.")
        return
    while (cur not in exitArea):
        cur = input("%s >>" % name)
        argShop = cur.split(",")
        if(argShop[0]!="" and argShop[0] not in exitArea):
            runShopCommands(argShop, name)
    print("exiting shop")
    shops.saveShops()

def getAllRegions():
    shopregions = shops.getShopRegions()
    itemregions = items.getItemRegions()
    print("Shop Regions: %s, Item Regions: %s" %(shopregions,itemregions))

def makeShop(args):
    for i in range(len(args)):
        args[i] = args[i].strip()
    name = args[0]
    shopType = args[1]
    city = args[2]
    region = args[3]
    wealth = args[4]
    shopItems = args[5].split(";")
    goldAmount = args[6]
    sellMult = args[7]
    tempShop = Shop(name,shopType,city,region,wealth,{},goldAmount,sellMult)

    for i in range(len(shopItems)):
        shopItems[i] = shopItems[i].strip()
        tempItem = items.getItemName(shopItems[i])
        tempShop.addNewItem(tempItem,1,tempItem.baseValue)
    shops.addShop(tempShop)
    shops.saveShops()


def manageRegions():
    cur = ""
    while cur not in exitArea:
        cur = input("Region Manager>>")
        argv = cur.split(",")
        for i in range(len(argv)):
            argv[i] = argv[i].strip()
        if argv[0] == "add shop region":
            regions.addNewShopRegion(argv[1])
        if argv[0] == "add item to shop region":
            regions.addItemRegion(argv[1],argv[2])
            regions.saveRegions()
            print(regions.regionManager)
        if argv[0] == "print regions":
            print(regions.regionManager)



if __name__ == '__main__':
    main()