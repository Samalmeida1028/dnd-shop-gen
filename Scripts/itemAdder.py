from Objects.TypeAndRegionManager import *

#just used to add new items to the item list

def main():
    items = ItemManager()
    userIn = " "
    while userIn != "exit":
        print("Enter item fields separated by a comma ( name, Item Type, Base Value, Rarity, Base Region)")
        print("Items separated by a ;")
        userIn = input(": ")
        if userIn != "exit":
            itemList = userIn.split(";")
            item = []
            for i in itemList:
                item = i.split(",")
                for i in range(len(item)):
                    item[i] = item[i].strip()
                print(item)
                if(len(item) == 5):
                    items.addItem(item)
                    items.saveItems()
                else:
                    print(len(item))
                    print("Error, incorrect formatting.")

        print("The item list now has " + str(len(list(items.itemList.keys()))) + " items.")


if __name__ == "__main__":
    main()