import string

from Objects.Shop import *
from Objects.TypeAndRegionManager import *


def main():
    items = ItemManager()  # manages the items.txt save file
    shops = ShopManager()  # manages the shops.txt save file
    types = TypeManager(shops, items)  # shop_type manager managers the item types that are offered by a shop shop_type
    regions = RegionManager(shops,items)
    print(types.typeManager)
    print(regions.regionManager)
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
    # region = input("Enter shop region and city separated by a ,").split()
    region = ['Fechura','Oksandarr','West Ozoa','East Ozoa','South East Ozoa','Magius','Crestus','Polar','Unknown Lands']
    for i in range(100):  # how many shops you want to create
        ii = random.randint(0,8)
        print("Shop number: ", i + 1)
        generateRegionalShops(region[ii], items, shops, types, nouns, nicknames, adjectives,regions,"")  # generates the shops by region and city, change the city and region name


def generateRegionalShops(shopRegion, items, shops, types, nouns, nicknames, adjectives, regions, city=""):
    name = random.randint(0, 2)  # more randomness for the name selection
    wealth = int(random.randint(1, 100))  # generates the wealth of the shop
    size = wealth * random.randint(5, 15)  # generates the base size of the shop
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
    print(shopName)  # just for testing
    generateRandomShop(shopName, city, shopRegion, size, wealth, items, shops,
                       types, regions)  # now generates the shop based on those attributes


def generateRandomShop(name, city, region, size, wealth, items, shops, types, regions):
    goldAmount = random.randint(1, 500) * wealth**1.5  # generates the amount of gold the shop has for items you sell to it
    if (wealth >= 1 and wealth < 50):  # determines the shop wealth for items
        wealth = "Poor"
    elif (wealth >= 50 and wealth < 80):
        wealth = "Middle Class"
    elif (wealth >= 80 and wealth < 95):
        wealth = "Wealthy"
    elif (wealth >= 95 and wealth < 100):
        wealth = "Elite"
    typesList = list(types.typeManager.keys())
    shopType = random.randint(0, len(typesList) - 1)
    shopType = typesList[shopType]
    sellRate = random.uniform(.1, .9)
    itemList = {}
    shop = Shop(str(name),"","", str(shopType), str(city), str(region), str(wealth), str(itemList), str(goldAmount),
                str(sellRate))
    types.saveTypes()
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
            shop.shopType]):  # checks if the item shop_type is found in the supported item types of the shop shop_type
            isAdded /= 2
            if (regions.regionList != "{}" and item.baseRegion in regions.regionManager[region]) or item.baseRegion == shop.region or item.baseRegion == "Anywhere":  # isAdded is divided according to the region and shop wealth to simulate the rarity being less in better and local shops
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
                cost = random.uniform(float(item.baseValue) / min(1.0,float(item.rarity)**1/4),
                                      float(item.baseValue) / min(.9,float(item.rarity)**1/3))
                if ((regions.regionList != "{}" and item.baseRegion in regions.regionManager[region]) or item.baseRegion == shop.region):  # if the item is in the region divide the cost by 2
                    cost /= 1.5
                shop.addNewItem(item, random.randint(1, int(float(isAdded) + float(item.rarity) + 2)),
                                # adds the new item to the shop
                                int(min(max(cost, 5), 1000000)))
        shops.addShop(shop)  # adds the shop to the shop list
        shops.saveShops()  # saves the shops to the text file


if __name__ == '__main__':
    main()
