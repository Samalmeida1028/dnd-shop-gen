from Objects.Shop import *
items = ItemManager()

shop = Shop()

manager = ShopManager()

shop.items = {}
shop.addNewItem(items.getItemName('Potion of Healing'), 5, 5)
print(vars(shop))
manager.addShop(shop)
manager.saveShops()