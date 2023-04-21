class Category:
    all = []
    def __init__(self, name, abbreviation, itemType, imgUrl = ''):
        self.name = name
        self.abbreviation = abbreviation
        self.typeType = itemType
        self.imgUrl = imgUrl
        
        # converting a number to a string for unification purposes
        self.id = str(len(self.all) + 1)

        Category.all.append(self)