from Objects.Shop import *
items = ItemManager()
shops = ShopManager('newFile.txt')
othershops = ShopManager()

temp_dict = {"name":"name","owner":"owner","notes":"notes","shop_type":"shop_type","city":"city","region":"region",
"wealth":"wealth","temp":"items","gold_amount":"gold_amount","sell_mult":"sell_mult"}



# copyDict = shops.shop_list
# for key in shops.shop_list:
#     updateDict = dict((temp_dict[key], value) for (key, value) in shops.shop_list[key].items())
#     copyDict[key] = updateDict

shops.shop_list = othershops.shop_list
shops.saveShops()