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
for line in adjectiveFile:
    adjectives = line.split(',')
adjectiveFile.close()
for line in nounFile:
    nouns = line.split(",")
nounFile.close()
for line in nicknameFile:
    nicknames = line.split(",")

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


def splitInput(userinput):
    argv = userinput.split(",")
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
                "Enter shop fields separated by a comma ([name],[shop_type],[city],[region],[wealth],[items],"
                "[gold amount],[sell multiplier]")
            print("Individual items should be separated by a ;")
            shop_in = input(": ")
            args = shop_in.split(",")
            if len(args) == 8:
                makeShop(args)
            else:
                print("invalid syntax for adding shop")
    else:
        print("command does not exist")


# ---------SHOP FUNCTIONS----------------
def buyShopItem(arg, shop_name):
    shops.getItemAmount(shop_name, arg[0])
    amount = 0
    cost = int(shops.getShopByName(shop_name)["Items"][arg[0]]["Cost"])
    print(cost)
    if len(arg) == 1:
        amount = 1
        shops.decreaseShopItemAmount(shop_name, arg[0])
        shops.increaseShopGoldAmount(shop_name, cost)
        if shops.getItemAmount(shop_name, arg[0]) == 0:
            shops.removeItem(shop_name, arg[0])
    elif len(arg) == 2:
        item_amount = int(shops.getItemAmount(shop_name, arg[0]))
        while amount < int(arg[1]) and amount < item_amount:
            shops.decreaseShopItemAmount(shop_name, arg[0])
            shops.increaseShopGoldAmount(shop_name, cost)
            if shops.getItemAmount(shop_name, arg[0]) == 0:
                shops.removeItem(shop_name, arg[0])
            amount += 1
    cost = amount * cost
    if int(cost) / 100 > 1:
        cost = str(cost / 100) + " gp"
    elif int(cost) / 10 > 1:
        cost = str(cost / 10) + " sp"
    else:
        cost = str(cost) + " cp"
    print("Bought %s %s for %s" % (amount, arg[0], cost))
    shops.saveShops()


def sellShopItem(arg, shop_name):
    amount = 1
    item_amount = 1
    shop = shops.shopList[shop_name]
    gold_amount = int(round(float(shop["GoldAmount"])))
    try:
        item = items.getItemName(arg[0])
    except KeyError:
        print("Item does not exist")
        return
    item_value = int(round(float(item.baseValue) * float(shop["SellMult"])))
    if item.item_type not in types.typeManager[shop["Type"]]:
        item_value /= 2
    if item.baseRegion not in regions.regionManager[shop["Region"]]:
        item_value *= 1.2
    item_value = int(round(item_value))
    if arg[0] in shop["Items"]:
        if len(arg) == 1:
            item_amount = 1
            shops.increaseShopItemAmount(shop_name, arg[0])
            shops.decreaseShopGoldAmount(shop_name, item_value)
        elif len(arg) == 2:
            item_amount = int(arg[1])
            while amount < item_amount and item_value < gold_amount:
                shops.increaseShopItemAmount(shop_name, arg[0])
                shops.decreaseShopGoldAmount(shop_name, item_value)
                gold_amount -= item_value
            item_amount = amount
        else:
            print("Invalid command structure.")
            return
    else:
        if len(arg) == 1:
            item_amount = 1
            shops.addNewItem(shop_name, item.name)
            shops.decreaseShopGoldAmount(shop_name, item_value)
        elif len(arg) == 2:
            item_amount = int(arg[1])
            shops.addNewItem(shop_name, item.name)
            amount = 1
            while amount < item_amount and gold_amount > 0:
                shops.increaseShopItemAmount(shop_name, arg[0])
                shops.decreaseShopGoldAmount(shop_name, item_value)
                gold_amount -= item_value
                amount += 1
            item_amount = amount
    cost = item_amount * item_value
    if int(cost) / 100 > 1:
        cost = str(cost / 100) + " gp"
    elif int(cost) / 10 > 1:
        cost = str(cost / 10) + " sp"
    else:
        cost = str(cost) + " cp"
    print("Sold %s %s(s) for %s" % (amount, arg[0], cost))


def runShopCommands(arg, shop_name):
    if arg[0] in buyItem:
        buyShopItem(arg[1:], shop_name)
    elif arg[0] in sellItem:
        sellShopItem(arg[1:], shop_name)
    elif arg[0] in printShop:
        shops.printShop(shop_name)
    else:
        print("command not found")


def currentShop(shop_name):
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


def makeShop(args):
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


def generateShops():
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
    for i in range(int(number)):
        makeShopRandom(type_shop, city, owner, region, wealth)
        print("%s: Generated successfully." % str(i + 1))


def makeShopRandom(type_shop, city, owner, region, wealth):
    region_list = list(regions.regionList)
    type_list = list(types.typeManager.keys())
    if wealth == "":
        wealth = random.randint(1, 100)
    else:
        wealth = wealth.split("-")
        if len(wealth) == 2:
            wealth = random.randint(int(wealth[0]), int(wealth[1]))
        else:
            wealth = random.randint(1, int(wealth[0]))
    if region == "":
        max_n = len(region_list)
        num = random.randint(0, max_n - 1)
        region = region_list[num]
    else:
        if region not in region_list:
            regions.addNewShopRegion(region)
    if type_shop == "":
        max_n = len(type_list)
        num = random.randint(0, max_n - 1)
        type_shop = type_list[num]
    else:
        if type_shop not in type_list:
            types.addNewShopType(type_shop)

    name = generateName()
    size = wealth * random.randint(5, 15)
    gold_amount = random.randint(1, 500) * wealth ** 1.5

    if 1 <= wealth < 50:  # determines the shop wealth for items
        wealth = "Poor"
    elif 50 <= wealth < 80:
        wealth = "Middle Class"
    elif 80 <= wealth < 95:
        wealth = "Wealthy"
    elif 95 <= wealth <= 100:
        wealth = "Elite"
    sell_rate = random.uniform(.1, .9)
    item_list = {}
    shop = Shop(name, owner, "", type_shop, city, region, str(wealth), item_list, str(int(gold_amount)), str(sell_rate))

    types.saveTypes()
    regions.saveRegions()

    for i in range(int(size)):
        item_index = random.randint(0, len(list(items.itemList.keys())))
        try:
            item = items.getItemIndex(int(item_index) - 1)  # picks a random item from the item list
        except IndexError:
            print("need to add items before you can run this file")
            break
        is_added = random.uniform(0, 100)
        # this is compared against the rarity of an item to determine if the item is added
        if any(item.item_type in shop_type for shop_type in types.typeManager[shop.shop_type]):
            # checks if the item shop_type is found in the supported item types of the shop shop_type
            is_added /= 2
            if (regions.regionList != "{}" and item.baseRegion in regions.regionManager[region]) \
                    or item.baseRegion == shop.region or item.baseRegion == "Anywhere":  # is_added is divided
                # according to the region and shop wealth to simulate the rarity being less in better and local shops
                is_added /= 2
            if wealth == "Elite":
                is_added /= 10
            elif wealth == "Wealthy":
                is_added /= 5
            elif wealth == "Middle Class":
                is_added /= 2
        else:  # if the item-shop_type is not offered by the shop then make it unlikely for the item to be in  the shop
            is_added *= 40
        if is_added <= float(item.rarity) <= is_added * 10:  # threshold for adding item to the shop pool
            if item.name in shop.items:
                shop.addItem(item.name, random.randint(1, int(float(is_added) + float(
                    item.rarity) + 2)))  # if the item is already in the shop then add more of it
            else:  # make the cost fluctuate around the base cost of the item
                cost = random.uniform(float(item.baseValue) / min(1.0, float(item.rarity) ** 1 / 4),
                                      float(item.baseValue) / min(.9, float(item.rarity) ** 1 / 3))
                if ((regions.regionList != "{}" and item.baseRegion in regions.regionManager[region])
                        or item.baseRegion == shop.region):  # if item is in the region divide the cost by 2
                    cost /= 1.5
                shop.addNewItem(item, random.randint(1, int(float(is_added) + float(item.rarity) + 2)),
                                # adds the new item to the shop
                                int(min(max(cost, 1), 1000000)))
        shops.addShop(shop)  # adds the shop to the shop list
        shops.saveShops()  # saves the shops to the text file


def generateName():
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
    print("Name: %s" % shop_name)
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
def printShopsIn(city):
    print("Printing shops in %s." % city)
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
          "----------------------------------------------------------------------------------------------------------\n"
          )



if __name__ == '__main__':
    main()
