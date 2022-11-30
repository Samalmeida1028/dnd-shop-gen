import string
from Objects.Shop import *
from Objects.TypeAndRegionManager import *
import os

shops = ShopManager()
items = ItemManager()
types = TypeManager(shops, items)
regions = RegionManager(shops, items)
nouns = []
adjectives = []
nicknames = []
types.saveTypes()
regions.saveRegions()
adjectiveFile = open("../Resources/names/adjectives.txt", "r")  # opens the list of adjectives for names
nicknameFile = open("../Resources/names/nicknames.txt", "r")  # opens the list of nicknames for names
nounFile = open("../Resources/names/nouns.txt", "r")  # opens the list of nouns for the names
# splits all the files into arrays for random name
for l in adjectiveFile:
    adjectives = l.split(',')
adjectiveFile.close()
for l in nounFile:
    nouns = l.split(",")
nounFile.close()
for l in nicknameFile:
    nicknames = l.split(",")

printShop = ['print', 'show']
printShopList = ['all', 'shops','l']
printShopIn = ["print shops in", "psi"]
enterShop = ['enter', 'visit', 'e', 'v']
buyItem = ['-', 'buy']
sellItem = ['+', 'sell']
exitArea = ['exit', 'leave']
regionCommand = ["regions"]
addCommand = ["add", "+"]
regionManager = ["edit regions", "manage regions"]
generateCom = ["generate", "make shops", "make", "gen", "gs"]
clearScreen = ["cls","clear"]
helpCommand = ["help", "h"]
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
        printAllShops()
        pass
    elif argv[0] in printShopIn:
        printShopsIn(argv[1])
    elif argv[0] in helpCommand:
        printHelp()
    elif argv[0] in printShop:
        shops.printShop(argv[1])
    elif argv[0] in enterShop:
        currentShop(argv[1])
    elif argv[0] in regionCommand:
        getAllRegions()
    elif argv[0] in regionManager:
        manageRegions()
    elif argv[0] in generateCom:
        generateShops()
    elif argv[0] in clearScreen:
        os.system('cls' if os.name == 'nt' else 'clear')
    elif argv[0] in addCommand:
        if argv[1] == "shop":
            print(
                "Enter shop fields separated by a comma ([name],[type],[city],[region],[wealth],[items],[gold amount],[sell multiplier]")
            print("Individual items should be separated by a ;")
            shopIn = input(": ")
            args = shopIn.split(",")
            if (len(args) == 8):
                makeShop(args)
            else:
                print("invalid syntax for adding shop")
    else:
        print("command does not exist")


def buyShopItem(arg, name):
    shops.getItemAmount(name, arg[0])
    amount = 0
    cost = int(shops.getShopbyName(name)["Items"][arg[0]]["Cost"])
    print(cost)
    if len(arg) == 1:
        amount = 1
        shops.decreaseShopItemAmount(name, arg[0])
        shops.increaseShopGoldAmount(name,cost)
        if shops.getItemAmount(name, arg[0]) == 0:
            shops.removeItem(name, arg[0])
    elif len(arg) == 2:
        itemAmount = int(shops.getItemAmount(name, arg[0]))
        while (amount < int(arg[1]) and amount < itemAmount):
            shops.decreaseShopItemAmount(name, arg[0])
            shops.increaseShopGoldAmount(name, cost)
            if shops.getItemAmount(name, arg[0]) == 0:
                shops.removeItem(name, arg[0])
            amount += 1
    cost = amount*cost
    if(int(cost)/100>1):
        cost = str(cost/100) + " gp"
    elif(int(cost)/10>1):
        cost = str(cost/10) + " sp"
    else:
        cost = str(cost) + " cp"
    print("Bought %s %s for %s" % (amount, arg[0],cost))
    shops.saveShops()


def sellShopItem(arg, name):
    shop = shops.shopList[name]
    goldAmount = int(round(float(shop["GoldAmount"])))
    try:
        item = items.getItemName(arg[0])
    except KeyError:
        print("Item does not exist")
        return
    itemValue = int(round(float(item.baseValue) * float(shop["SellMult"])))
    if (item.itemType not in types.typeManager[shop["Type"]]):
        itemValue /= 2
    if (item.baseRegion not in regions.regionManager[shop["Region"]]):
        itemValue *= 1.2
    itemValue = int(round(itemValue))
    if (arg[0] in shop["Items"]):
        if len(arg) == 1:
            itemAmount = 1
            shops.increaseShopItemAmount(name, arg[0])
            shops.decreaseShopGoldAmount(name, itemValue)
        elif len(arg) == 2:
            itemAmount = int(arg[1])
            amount = 0
            while amount < itemAmount and itemValue < goldAmount:
                shops.increaseShopItemAmount(name, arg[0])
                shops.decreaseShopGoldAmount(name, itemValue)
                goldAmount -= itemValue
                amount += 1
            itemAmount = amount
        else:
            print("Invalid command structure.")
            return
    else:
        if len(arg) == 1:
            itemAmount = 1
            shops.addNewItem(name, item.name)
            shops.decreaseShopGoldAmount(name, itemValue)
        elif len(arg) == 2:
            itemAmount = int(arg[1])
            shops.addNewItem(name, item.name)
            amount = 1
            while amount < itemAmount and goldAmount > 0:
                shops.increaseShopItemAmount(name, arg[0])
                shops.decreaseShopGoldAmount(name, itemValue)
                goldAmount -= itemValue
                amount += 1
            itemAmount = amount
    cost = itemAmount * itemValue
    if (int(cost) / 100 > 1):
        cost = str(cost / 100) + " gp"
    elif (int(cost) / 10 > 1):
        cost = str(cost / 10) + " sp"
    else:
        cost = str(cost) + " cp"
    print("Sold %s %s(s) for %s" % (amount, arg[0], cost))


def runShopCommands(arg, name):
    if arg[0] in buyItem:
        buyShopItem(arg[1:], name)
    elif arg[0] in sellItem:
        sellShopItem(arg[1:], name)
    elif arg[0] in printShop:
        shops.printShop(name)
    else:
        print("command not found")


def currentShop(name):
    name = name.strip()
    cur = ""
    try:
        shops.printShop(name)
    except KeyError:
        print("Shop does not exist.")
        return
    while (cur not in exitArea):
        cur = input("%s >>" % name)
        argShop = cur.split(",")
        if (argShop[0] != "" and argShop[0] not in exitArea):
            runShopCommands(argShop, name)
    print("exiting shop")
    shops.saveShops()


def getAllRegions():
    shopregions = shops.getShopRegions()
    itemregions = items.getItemRegions()
    print("Shop Regions: %s, Item Regions: %s" % (shopregions, itemregions))


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
    tempShop = Shop(name, shopType, city, region, wealth, {}, goldAmount, sellMult)

    for i in range(len(shopItems)):
        shopItems[i] = shopItems[i].strip()
        tempItem = items.getItemName(shopItems[i])
        tempShop.addNewItem(tempItem, 1, tempItem.baseValue)
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
            regions.addItemRegion(argv[1], argv[2])
            regions.saveRegions()
            print(regions.regionManager)
        if argv[0] == "print regions":
            print(regions.regionManager)


def generateShops():
    print("For all inputs dont enter anything to default to random generation")
    region = input("Enter region: ")
    city = input("Enter city: ")
    owner = input("Enter owner: ")
    print("Enter wealth separated by a '-' if you want a range (1-100)")
    wealth = input("Enter wealth (1 being lowest, 100 being highest): ")
    typeShop = input("Enter type: ")
    number = input("Enter number of shops to create: ")
    if (number == ""):
        number = 1
    for i in range(int(number)):
        makeShopRandom(typeShop, city, owner, region, wealth)
        print("%s: Generated successfully." % str(i + 1))


def makeShopRandom(typeShop, city, owner, region, wealth):
    regionList = list(regions.regionList)
    typeList = list(types.typeManager.keys())
    if wealth == "":
        wealth = random.randint(1, 100)
    else:
        wealth = wealth.split("-")
        if len(wealth) == 2:
            print("hellogen"
                  "")
            wealth = random.randint(int(wealth[0]), int(wealth[1]))
        else:
            wealth = random.randint(1, int(wealth[0]))
    if region == "":
        maxN = len(regionList)
        num = random.randint(0, maxN - 1)
        region = regionList[num]
    else:
        if region not in regionList:
            regions.addNewShopRegion(region)
    if typeShop == "":
        maxN = len(typeList)
        num = random.randint(0, maxN - 1)
        typeShop = typeList[num]
    else:
        if typeShop not in typeList:
            types.addNewShopType(typeShop)

    name = generateName()
    size = wealth * random.randint(5, 15)
    goldAmount = random.randint(1, 500) * wealth ** 1.5
    if (wealth >= 1 and wealth < 50):  # determines the shop wealth for items
        wealth = "Poor"
    elif (wealth >= 50 and wealth < 80):
        wealth = "Middle Class"
    elif (wealth >= 80 and wealth < 95):
        wealth = "Wealthy"
    elif (wealth >= 95 and wealth <= 100):
        wealth = "Elite"
    sellRate = random.uniform(.1, .9)
    itemList = {}
    shop = Shop(name, owner, "", typeShop, city, region, str(wealth), itemList, str(int(goldAmount)), str(sellRate))
    types.saveTypes()
    regions.saveRegions()

    for i in range(int(size)):
        itemIndex = random.randint(0, len(list(items.itemList.keys())))
        try:
            item = items.getItemIndex(int(itemIndex) - 1)  # picks a random item from the item list
        except IndexError:
            print("need to add items before you can run this file")
            break
        isAdded = random.uniform(0,
                                 100)  # this is compared against the rarity of an item to determine if the item is added
        if any(item.itemType in type for type in types.typeManager[
            shop.shopType]):  # checks if the item type is found in the supported item types of the shop type
            isAdded /= 2
            if (regions.regionList != "{}" and item.baseRegion in regions.regionManager[
                region]) or item.baseRegion == shop.region or item.baseRegion == "Anywhere":  # isAdded is divided according to the region and shop wealth to simulate the rarity being less in better and local shops
                isAdded /= 2
            if wealth == "Elite":
                isAdded /= 10
            elif wealth == "Wealthy":
                isAdded /= 5
            elif wealth == "Middle Class":
                isAdded /= 2
        else:  # if the itemtype is not offered by the shop then make it very unlikely for the item to be in the shop
            isAdded *= 40
        if isAdded <= float(item.rarity) and isAdded * 10 >= float(
                item.rarity):  # check to see if the item is added (also says if isAdded is 10 times less than dont add the item)
            if (item.name in shop.items):
                shop.addItem(item.name, random.randint(1, int(float(isAdded) + float(
                    item.rarity) + 2)))  # if the item is already in the shop then add more of it
            else:  # make the cost fluctuate around the base cost of the item
                cost = random.uniform(float(item.baseValue) / min(1.0, float(item.rarity) ** 1 / 4),
                                      float(item.baseValue) / min(.9, float(item.rarity) ** 1 / 3))
                if ((regions.regionList != "{}" and item.baseRegion in regions.regionManager[
                    region]) or item.baseRegion == shop.region):  # if the item is in the region divide the cost by 2
                    cost /= 1.5
                shop.addNewItem(item, random.randint(1, int(float(isAdded) + float(item.rarity) + 2)),
                                # adds the new item to the shop
                                int(min(max(cost, 1), 1000000)))
        shops.addShop(shop)  # adds the shop to the shop list
        shops.saveShops()  # saves the shops to the text file


def generateName():
    name = random.randint(0, 2)  # more randomness for the name selection
    pickNoun = random.randint(0, len(nouns) - 1)  # picks a random noun for the name
    if name == 0:
        pickAdjective = random.randint(0, len(adjectives) - 1)  # picks a random adjective for the name
        shopName = "The" + adjectives[pickAdjective].strip('"') + " " + nouns[pickNoun].strip(
            '"')  # The [adjective] [noun] name
        shopName = string.capwords(shopName)
    elif name == 1:
        shopName = nicknames[random.randint(0, len(nicknames) - 1)].strip(",") + "'s"  # [Nickname]'s name
    else:
        shopName = nicknames[random.randint(0, len(nicknames) - 1)].strip(",") + "'s "  # [Nicknames]'s [noun] name
        shopName += string.capwords(nouns[pickNoun].strip('"'))
    print("Name: %s" % shopName)
    return shopName


def printShopsIn(city):
    print("Printing shops in %s."% city)
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    allRegions = list(shops.getShopRegions())
    shopsIn = list(shops.getShopByCity(city).keys())
    if city in allRegions:
        shopsIn = list(shops.getShopByRegion(city))
    count = 1
    for k in shopsIn:
        shop = shops.getShopbyName(k)
        stringPrint = "| #" + str(count) + ", Shop : " + k + " | Region : " + shop["Region"] + " | City : " + shop["City"] + " |" + " | Wealth : " + shop["Wealth"] + " |"
        stringSep = "-."*int((len(stringPrint)/2))
        print(stringPrint)
        print(stringSep)
        count+=1
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")


def printAllShops():
    shopsToPrint = list(shops.shopList.keys())
    count = 1
    for k in shopsToPrint:
        shop = shops.getShopbyName(k)
        stringPrint = "| #" + str(count) + ", Shop : " + k + " | Region : " + shop["Region"] + " | City : " + shop["City"] + " | Wealth : " + shop["Wealth"] + " |"
        stringSep = "-."*int((len(stringPrint)/2))
        print(stringPrint)
        print(stringSep)
        count+=1

def printHelp():
    print("All arguments should be separated by a ',', [] indicated required argument, {} indicates optional argument"
          "\nCommands are: \n"
          "print,[Shop Name]: prints the shop given a name\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "all: prints all shops\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "print shops in,[Region/City]: prints shops in a given region or city\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "enter,[Shop Name]: Enters a shop\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "(in shop) buy,[Item],{Amount}: buys x amount of item from a shop\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "(in shop) sell,[Item],{Amount}: sells x amount of item from a shop\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "exit: exits area/terminal\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "regions: gets all shop regionn"
          "add: adds new shop\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "edit regions: opens the edit region\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "(in region manager) add shop region: adds a new region\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "(in region manager) add item to region: adds a new item to a region\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "(in region manager) print regions: prints all regions\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "generate: enters shop generator\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "cls: clears screen\n"
          "----------------------------------------------------------------------------------------------------------\n"
          "help: prints out list of commands\n"
          "----------------------------------------------------------------------------------------------------------h\n")



if __name__ == '__main__':
    main()
