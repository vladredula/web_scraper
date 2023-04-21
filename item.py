
class Item:
    all = []
    def __init__(self, name, tname, category, subCategory, itemType, price, imgUrl = ""):
        self.name = name
        self.tname = tname
        self.price = price
        self.category = category
        self.subcategory = subCategory
        self.imgUrl = imgUrl
        self.typeType = itemType
        self.id = len(self.all) + 1

        Item.all.append(self)

    #def __repr__(self):
    #    return f'{self.__class__.__name__},{self.name}/{self.tname},{self.desc},{self.price}'