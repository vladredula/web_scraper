
class Item:
    all = []
    def __init__(self, name, tname, description, price, category, subcategory, img_url):
        self.name = name
        self.tname = tname
        self.description = description
        self.price = price
        self.category = category
        self.subcategory = subcategory
        self.img_url = img_url

        Item.all.append(self)

    #def __repr__(self):
    #    return f'{self.__class__.__name__},{self.name}/{self.tname},{self.desc},{self.price}'