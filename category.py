class Category:
    all = []
    def __init__(self, name, abbreviation, itemType, imgUrl = ""):
        self.name = name
        self.abbreviation = abbreviation
        self.itemType = itemType
        self.imgUrl = imgUrl
        self.id = len(self.all) + 1

        Category.all.append(self)