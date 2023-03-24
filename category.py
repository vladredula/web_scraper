class Category:
    all = []
    def __init__(self, name, abbreviation, itemtype, img_url = ''):
        self.name = name
        self.abbreviation = abbreviation
        self.type = itemtype
        self.img_url = img_url
        
        # converting a number to a string for unification purposes
        self.id = str(len(self.all) + 1)

        Category.all.append(self)