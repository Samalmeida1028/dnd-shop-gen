import os
import string
import threading
import time

from Objects.Shop import *
from Objects.TypeAndRegionManager import *
# ---GOLBALS---
REGION_ITEM_VALUE = 1.2  # used to determine how an item's value fluctuates based on region
TYPE_ITEM_VALUE = 2  # used to determine item's price when sold if it is in the shop that sells it
ELITE_RARITY_MULT = 10  # this number dictates the rarity of item found in elite shops, higher means more rare items
MIN_SELL_MULT = .1
MAX_SELL_MULT = .9

WEALTHY_RARITY_MULT = 5  # this number dictates the rarity of item found in wealthy shops, higher means more rare items
MIDDLECLASS_RARITY_MULT = 2  # this number dictates the rarity of item found in middle class shops,
                                                # higher means more rare items
POOR_RARITY_MULT = 1 # ^^^

POOR_CHANCE = 50
MIDDLECLASS_CHANCE = 30
WEALTHY_CHANCE = 15
ELITE_CHANCE = 5
TOTAL_THRESH = (POOR_CHANCE+MIDDLECLASS_CHANCE+WEALTHY_CHANCE+ELITE_CHANCE)


MAX_ITEM_COST = 1000000

#-------------
#----SET UP----
shops = ShopManager()
shop_names = list(shops.shopList.keys())
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
for line in adjectiveFile:
    adjectives = line.split(',')
adjectiveFile.close()
for line in nounFile:
    nouns = line.split(",")
nounFile.close()
for line in nicknameFile:
    nicknames = line.split(",")
#----------------

# lists for the command to add the option for custom command input and shortcuts
printShop = ['print', 'show']
printShopList = ['all', 'shops', 'l']
printShopIn = ["print shops in", "psi"]
enterShop = ['enter', 'visit', 'e', 'v']
buyItem = ['-', 'buy']
sellItem = ['+', 'sell']
exitArea = ['exit', 'leave']
regionCommand = ["regions"]
addCommand = ["add", "+"]
regionManager = ["edit regions", "manage regions"]
generateCom = ["generate", "make shops", "make", "gen", "gs"]
clearScreen = ["cls", "clear"]
helpCommand = ["help", "h"]


def main():
    userinput = ""
    while userinput not in exitArea:
        userinput = input(">> ")
        argv = splitInput(userinput)
        if userinput not in exitArea:
            runCommands(argv)


def splitInput(userinput: str):
    argv = userinput.split(",")
    return argv


def runCommands(argv: list):  # simple interface with if statements to run commands that the user inputs
    if argv[0] in printShopList:
        printAllShops()
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
        os.system('cls' if os.name == 'nt' else 'clear')  # clears screen
    elif argv[0] in addCommand:
        if (len(argv[0]) != 2):
            print("Invalid structure for 'add'")
        if argv[1] == "shop":
            print(
                "Enter shop fields separated by a comma ([name],[shop_type],[city],[region],[wealth],[items],"
                "[gold amount],[sell multiplier]")
            print("Individual items should be separated by a ;")
            shop_in = input(": ")
            args = shop_in.split(",")
            if len(args) == 8:
                makeShop(args)
            else:
                print("invalid syntax for adding shop")

        elif argv[1] == "item":
            print(
                "Enter item fields separated by a comma ([name],[type],[value],[rarity],[Base Region]")
            print("Individual items should be separated by a ;")
            item_in = input(": ")
            args = item_in.split(",")
            if len(args) == 5:
                items.addItem(args)
                items.saveItems()
            else:
                print("invalid syntax for adding item")
    else:
        print("command does not exist")


# ---------SHOP FUNCTIONS----------------
def buyShopItem(arg: list, shop_name: str):  # buys an item in a shop
    try:
        shop = shops.shopList[shop_name]
    except KeyError:
        print("Shop does not exist")
        return
    try:
        item = items.getItemName(arg[0])
    except KeyError:
        print("Item does not exist")
        return

    item_amount = int(shops.getItemAmount(shop_name, arg[0]))  # gets the amount of an item that the given shop has
    amount = 0
    cost = int(shops.getShopByName(shop_name)["Items"][arg[0]]["Cost"])  # gets the cost of the item in the shop
    if len(arg) == 1:  # determines if the user is buying 1 of them or multiple
        amount = 1
        shops.decreaseShopItemAmount(shop_name, arg[0])
        shops.increaseShopGoldAmount(shop_name, cost)  # increases the gold amount of the shop when an item is bought
        if shops.getItemAmount(shop_name, arg[0]) == 0:  # if the item amount is 0 then remove the item
            shops.removeItem(shop_name, arg[0])
    elif len(arg) == 2:  # this is for when the use inputs that they want multiple items
        while amount < int(arg[1]) and amount < item_amount:  # loops until either the amount of items is bought or
            shops.decreaseShopItemAmount(shop_name, arg[0])  # until the shop runs out of that item
            shops.increaseShopGoldAmount(shop_name, cost)  # increases shop gold amount
            if shops.getItemAmount(shop_name, arg[0]) == 0:  # removes the item if the item amount drops to 0
                shops.removeItem(shop_name, arg[0])
            amount += 1
    cost = amount * cost  # gives the total cost of the item
    if int(cost) / 100 > 1:  # translates it to gold pieces, as all my items in the list are cp
        cost = str(cost / 100) + " gp"
    elif int(cost) / 10 > 1:
        cost = str(cost / 10) + " sp"
    else:
        cost = str(cost) + " cp"
    print("Bought %s %s for %s" % (amount, arg[0], cost))  # prints the amount of an item bought
    shops.saveShops()


def sellShopItem(arg: list, shop_name: str):  # sells an item to the shop
    # error handling for bad inputs
    try:
        shop = shops.shopList[shop_name]
    except KeyError:
        print("Shop does not exist")
        return
    try:
        item = items.getItemName(arg[0])
    except KeyError:
        print("Item does not exist")
        return

    amount = 1  # sets both the amount and item amount for future use
    item_amount = 1
    gold_amount = int(round(float(shop["GoldAmount"])))  # finds the gold amount of the shop given
    item_value = int(round(float(item.baseValue) * float(shop["SellMult"])))  # gets the value of item being sold

    if item.itemType not in types.typeManager[shop["Type"]]: # checks to see if the type is sold in the shop
        item_value /= TYPE_ITEM_VALUE
    if item.baseRegion not in regions.regionManager[shop["Region"]]: # checks to see if the shop is in the item region
        item_value *= REGION_ITEM_VALUE

    item_value = int(round(item_value))

    if arg[0] in shop["Items"]: # sells the item to the shop if the shop has the item already
        if len(arg) > 2:
            print('Invalid command')
            return
        if len(arg) == 1:
            item_amount = 1
            shops.increaseShopItemAmount(shop_name, arg[0])
            shops.decreaseShopGoldAmount(shop_name, item_value)
        elif len(arg) == 2:
            item_amount = int(arg[1])
            while amount < item_amount and item_value < gold_amount: # goes until either you sell the right amount
                shops.increaseShopItemAmount(shop_name, arg[0])             # or the shop runs out of money
                shops.decreaseShopGoldAmount(shop_name, item_value)
                gold_amount -= item_value
            item_amount = amount
    else: # sells item to the shop if it doesn't have the item already
        if len(arg) > 2:
            print('Invalid command')
            return
        if len(arg) == 1:
            item_amount = 1
            shops.addNewItem(shop_name, item.name)
            shops.decreaseShopGoldAmount(shop_name, item_value)
        elif len(arg) == 2:
            item_amount = int(arg[1])
            shops.addNewItem(shop_name, item.name)
            amount = 1
            while amount < item_amount and gold_amount > 0: # goes until you sell the right amount
                shops.increaseShopItemAmount(shop_name, arg[0])             # or the shop runs out of money
                shops.decreaseShopGoldAmount(shop_name, item_value)
                gold_amount -= item_value
                amount += 1
            item_amount = amount

    cost = item_amount * item_value # finds how much the sale was worth
    if int(cost) / 100 > 1:
        cost = str(cost / 100) + " gp"
    elif int(cost) / 10 > 1:
        cost = str(cost / 10) + " sp"
    else:
        cost = str(cost) + " cp"
    print("Sold %s %s(s) for %s" % (amount, arg[0], cost))


def runShopCommands(arg: list, shop_name: str): # for running shop commands
    if arg[0] in buyItem:
        buyShopItem(arg[1:], shop_name)
    elif arg[0] in sellItem:
        sellShopItem(arg[1:], shop_name)
    elif arg[0] in printShop:
        shops.printShop(shop_name)
    else:
        print("command not found")


def currentShop(shop_name: str): # runs a prompt with the current shop for doing shop commands
    shop_name = shop_name.strip()
    cur = ""
    try:
        shops.printShop(shop_name)
    except KeyError:
        print("Shop does not exist.")
        return
    while cur not in exitArea:
        cur = input("%s >>" % shop_name)
        arg_shop = cur.split(",")
        if arg_shop[0] != "" and arg_shop[0] not in exitArea:
            runShopCommands(arg_shop, shop_name)
    print("exiting shop")
    shops.saveShops()


def makeShop(args: list): # makes a shop given a list of arguments
    for i in range(len(args)):
        args[i] = args[i].strip()
    shop_name = args[0]
    shop_type = args[1]
    city = args[2]
    region = args[3]
    wealth = args[4]
    shop_items = args[5].split(";")
    gold_amount = args[6]
    sell_mult = args[7]
    temp_shop = Shop(shop_name, shop_type, city, region, wealth, {}, gold_amount, sell_mult)

    for i in range(len(shop_items)):
        shop_items[i] = shop_items[i].strip()
        temp_item = items.getItemName(shop_items[i])
        temp_shop.addNewItem(temp_item, 1, temp_item.baseValue)
    shops.addShop(temp_shop)
    shops.saveShops()


def generateShops(): # prompts the user for shop generation
    print("For all inputs dont enter anything to default to random generation")
    region = input("Enter region: ")
    city = input("Enter city: ")
    owner = input("Enter owner: ")
    print("Enter wealth separated by a '-' if you want a range (1-100)")
    wealth = input("Enter wealth (1 being lowest, 100 being highest): ")
    type_shop = input("Enter shop_type: ")
    number = input("Enter number of shops to create: ")
    if number == "":
        number = 1
    threadList = []
    st = time.time()
    integers = range(int(number))

    for i in integers:
        thread = threading.Thread(target=makeShopRandom, args=(type_shop, city, owner, region, wealth))
        # makeShopRandom(type_shop, city, owner, region, wealth)
        thread.start()
        threadList.append(thread)
    for thread in threadList:
        thread.join()
    shops.saveShops()  # saves the shops to the text file
    types.saveTypes()
    regions.saveRegions()
    et = time.time()
    print("Total time was: %s." % (et - st))


def makeShopRandom(type_shop: str, city: str, owner: str, region: str, wealth: str):
    region_list = list(regions.regionList) # gets a list of the regions from the text file
    type_list = list(types.typeManager.keys()) # gets a list of the types of shops from the text file
    if wealth == "":
        wealth = random.randint(1, 100) # this determines the wealth of the shop based on the presets
    else:
        wealth = wealth.split("-") # if the user entered a range use that
        if len(wealth) == 2:
            wealth = random.randint(max(1,int(wealth[0])), min(100,int(wealth[1]))) # assures shop thresh is 1-100
        else:
            wealth = random.randint(1, min(100,int(wealth[0])))
    if region == "": # if the region is not given select a random region
        max_n = len(region_list)
        num = random.randint(0, max_n - 1)
        region = region_list[num]
    else:
        if region not in region_list: # if the region isn't in the list already add it
            regions.addNewShopRegion(region)
    if type_shop == "": # if the type of shop isn't given then randomly assign it
        max_n = len(type_list)
        num = random.randint(0, max_n - 1)
        type_shop = type_list[num]
    else:
        if type_shop not in type_list: # if the type given is not in the type list add it
            types.addNewShopType(type_shop)

    name = generateName() # generate's the name of the shop and the key
    size = wealth * random.randint(5, 15) # generates a shop of a random size influenced by the wealth
    gold_amount = random.randint(1, 500) * wealth ** 1.5 # makes the random gold amount influenced by wealth

    # these are generating the thresholds out of 100 to allow for the percentages to make sense
    poor_thresh = round((POOR_CHANCE/TOTAL_THRESH)*100)
    middleclass_thresh = poor_thresh + round((MIDDLECLASS_CHANCE/TOTAL_THRESH)*100)
    wealthy_thresh = middleclass_thresh + round((WEALTHY_CHANCE/TOTAL_THRESH)*100)
    elite_thresh = wealthy_thresh + round((ELITE_CHANCE/TOTAL_THRESH)*100)

    if 0 <= wealth < poor_thresh:  # determines the shop wealth for items
        wealth = "Poor"
    elif poor_thresh <= wealth < middleclass_thresh:
        wealth = "Middle Class"
    elif middleclass_thresh <= wealth < wealthy_thresh:
        wealth = "Wealthy"
    elif wealthy_thresh <= wealth <= elite_thresh:
        wealth = "Elite"
    sell_rate = random.uniform(MIN_SELL_MULT, MAX_SELL_MULT) # determines the sell multiplier of a shop
    item_list = {}
    # creates the shop with an empty item list
    shop = Shop(name, owner, "", type_shop, city, region, str(wealth), item_list, str(int(gold_amount)), str(sell_rate))

    for i in range(int(size)): ## this is how many times it tries to add items to the shop
        item_index = random.randint(0, len(list(items.itemList.keys())))
        try:
            item = items.getItemIndex(int(item_index) - 1)  # picks a random item from the item list
        except IndexError:
            print("need to add items before you can run this file")
            break
        can_be_added = random.uniform(0, 100)
        # this is compared against the rarity of an item to determine if the item is added
        if any(item.item_type in shop_type for shop_type in types.typeManager[shop.shop_type]):
            # checks if the item shop_type is found in the supported item types of the shop shop_type
            can_be_added /= 2
            if (regions.regionList != "{}" and item.baseRegion in regions.regionManager[region]) \
                    or item.baseRegion == shop.region or item.baseRegion == "Anywhere":  # can_be_added is divided
                # according to the region and shop wealth to simulate the rarity being less in better and local shops
                can_be_added /= 2
            if wealth == "Elite":
                can_be_added /= ELITE_RARITY_MULT
            elif wealth == "Wealthy":
                can_be_added /= WEALTHY_RARITY_MULT
            elif wealth == "Middle Class":
                can_be_added /= MIDDLECLASS_RARITY_MULT
            elif wealth == "Poor":
                can_be_added /= POOR_RARITY_MULT
        else:  # if the item-shop_type is not offered by the shop then make it unlikely for the item to be in  the shop
            can_be_added *= 40
        if can_be_added <= float(item.rarity) <= can_be_added * 10:  # threshold for adding item to the shop pool
            if item.name in shop.items:
                shop.addItem(item.name, random.randint(1, int(float(can_be_added) + float(
                    item.rarity) + 2)))  # if the item is already in the shop then add more of it
            else:  # make the cost fluctuate around the base cost of the item
                cost = random.uniform(float(item.baseValue) / min(1.0, float(item.rarity) ** 1 / 4),
                                      float(item.baseValue) / min(.9, float(item.rarity) ** 1 / 3))
                if ((regions.regionList != "{}" and item.baseRegion in regions.regionManager[region])
                        or item.baseRegion == shop.region):  # if item is in the region divide the cost by 1.2
                    cost /= REGION_ITEM_VALUE
                shop.addNewItem(item, str(random.randint(1, int(float(can_be_added) + float(item.rarity) + 2))),
                                int(min(max(cost, 1), MAX_ITEM_COST)))
        shops.addShop(shop)  # adds the shop to the shop list
        # shops.saveShops()


def generateName():
    if (len(shop_names) != 0):
        shop_name = shop_names[0]
        while shop_name in shops.shopList:
            shop_name = random.randint(0, 2)  # more randomness for the name selection
            pick_noun = random.randint(0, len(nouns) - 1)  # picks a random noun for the name
            if shop_name == 0:
                pick_adjective = random.randint(0, len(adjectives) - 1)  # picks a random adjective for the name
                shop_name = "The" + adjectives[pick_adjective].strip('"') + " " + nouns[pick_noun].strip(
                    '"')  # The [adjective] [noun] name
                shop_name = string.capwords(shop_name)
            elif shop_name == 1:
                shop_name = nicknames[random.randint(0, len(nicknames) - 1)].strip(",") + "'s"  # [Nickname]'s name
            else:
                shop_name = nicknames[random.randint(0, len(nicknames) - 1)].strip(
                    ",") + "'s "  # [Nicknames]'s [noun] name
                shop_name += string.capwords(nouns[pick_noun].strip('"'))
    else:
        shop_name = random.randint(0, 2)  # more randomness for the name selection
        pick_noun = random.randint(0, len(nouns) - 1)  # picks a random noun for the name
        if shop_name == 0:
            pick_adjective = random.randint(0, len(adjectives) - 1)  # picks a random adjective for the name
            shop_name = "The" + adjectives[pick_adjective].strip('"') + " " + nouns[pick_noun].strip(
                '"')  # The [adjective] [noun] name
            shop_name = string.capwords(shop_name)
        elif shop_name == 1:
            shop_name = nicknames[random.randint(0, len(nicknames) - 1)].strip(",") + "'s"  # [Nickname]'s name
        else:
            shop_name = nicknames[random.randint(0, len(nicknames) - 1)].strip(",") + "'s "  # [Nicknames]'s [noun] name
            shop_name += string.capwords(nouns[pick_noun].strip('"'))
    shop_names.append(shop_name)
    # print("Name: %s" %(shop_name))
    return shop_name


# -----------REGION FUNCTIONS----------------
def manageRegions():
    current_input = ""
    while current_input not in exitArea:
        current_input = input("Region Manager>>")
        argv = current_input.split(",")
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


def getAllRegions():
    shop_regions = shops.getShopRegions()
    item_regions = items.getItemRegions()
    print("Shop Regions: %s, Item Regions: %s" % (shop_regions, item_regions))


# -----------------PRINT FUNCTIONS--------------------
def printShopsIn(city: str):
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    all_regions = list(shops.getShopRegions())
    shops_in = list(shops.getShopByCity(city).keys())
    if city in all_regions:
        shops_in = list(shops.getShopByRegion(city))
    count = 1
    for k in shops_in:
        shop = shops.getShopByName(k)
        string_print = "| #" + str(count) + ", Shop : " + k + " | Region : " + shop["Region"] + " | City : " + shop[
            "City"] + " |" + " | Wealth : " + shop["Wealth"] + " |"
        string_sep = "-." * int((len(string_print) / 2))
        print(string_print)
        print(string_sep)
        count += 1
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")


def printAllShops():
    shops_to_print = list(shops.shopList.keys())
    count = 1
    for k in shops_to_print:
        shop = shops.getShopByName(k)
        string_print = "| #" + str(count) + ", Shop : " + k + " | Region : " + shop["Region"] + " | City : " + shop[
            "City"] + " | Wealth : " + shop["Wealth"] + " |"
        string_sep = "-." * int((len(string_print) / 2))
        print(string_print)
        print(string_sep)
        count += 1


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
          "regions: gets all shop region"
          "----------------------------------------------------------------------------------------------------------\n"
          "add, shop/item: adds new shop/item depending on which is inputted by the user\n"
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
          "----------------------------------------------------------------------------------------------------------\n"
          )


if __name__ == '__main__':
    main()
