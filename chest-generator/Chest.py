from Objects.Item import *


class RandomChest:
    def __init__(self,chest_rarity : int) -> int:
        if 0 > chest_rarity:
            self.rarity = 0
        elif chest_rarity > 1000:
            self.rarity = 1000
        else:
            self.rarity = chest_rarity
        #generateChest(self.rarity)
