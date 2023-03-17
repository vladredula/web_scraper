
class Item:
    all = []
    def __init__(self, name, tname, description, price):
        self.name = name
        self.tname = tname
        self.description = description
        self.price = price

        Item.all.append(self)

    #def __repr__(self):
    #    return f'{self.__class__.__name__},{self.name}/{self.tname},{self.desc},{self.price}'


class Food(Item):
    all = []
    def __init__(self, name, tname, description, price, category, subcategory = None):
        # Call to super function to have access to all attributes / methods
        super().__init__(
            name, tname, description, price
        )

        # Assign to self object
        self.category = category
        self.subcategory = subcategory

        Food.all.append(self)


class Drink(Item):
    all = []
    def __init__(self, name, tname, description, price, category, subcategory = None):
        # Call to super function to have access to all attributes / methods
        super().__init__(
            name, tname, description, price
        )

        # Assign to self object
        self.category = category
        self.subcategory = subcategory

        Drink.all.append(self)