from bs4 import BeautifulSoup
import requests
import re
from item import Item
from category import Category

def getContent(url):
    """
    Sends a get request to the url and parses the response
    @param url (str): URL of the web page to be parsed
    @returns: bs4 object
    """
    response = requests.get(url)
    content = response.content
    content = BeautifulSoup(content, "html.parser")
    
    return content


def getStrippedString(string):
    """
    Strips off html tags using bs4's stripped_strings function
    @param: str
    @returns: list of parsed string
    """
    string = string.stripped_strings
    
    return list(string)


def getPrices(priceString): 
    """
    Locates and identifies the sizes and prices based on the patterns obseved.
    @param: priceString (str)
    @returns: String containing only the sizes and corresponding prices
        ex: 'size1:price1,size2:price2'
    """
    # replacing japanese characters with english equivalent words
    priceString = priceString.replace("（", "(")
    priceString = priceString.replace("）", ")")
    priceString = priceString.replace(",", "")
    priceString = priceString.replace("グラス", "glass")
    priceString = priceString.replace("ハーフボトル", "halfbottle")
    priceString = priceString.replace("ボトル", "bottle")
    priceString = priceString.replace("ハーフサイズ", "half")
    priceString = priceString.replace("レギュラーサイズ", "regular")
    priceString = priceString.replace("フルサイズ", "full")

    # available patterns
    patterns = [r"\((\w)\)(\d+)円\(税込(\d+)", 
                r"(\d\w)\ (\d+)円\(税込(\d+)", 
                r"(\w+)\:(\d+)円\(税込(\d+)", 
                r"(\w+)\ (\d+)円\(税込(\d+)", 
                r"([a-z]+)([0-9]+)円\(税込(\d+)", 
                r"(\d+)円\(税込(\d+)",
                r"(\d+)円\ \(税込(\d+)"
    ]

    prices = []
    for pattern in patterns:
        matches = re.findall(pattern, priceString)
        if matches != None and matches != []:
            for match in matches:
                if len(match) == 2:
                    prices.append("1:"+match[1])
                else:
                    prices.append(match[0]+":"+match[2])
            break
    
    return ",".join(prices)


def makeAbbreviation(string):
    """
    Makes abrreviation of a string
    @params: string (str)
    @returns: String abbreviation
    """
    if string == '':
        return string
        
    # remove white space
    string = string.strip()

    # use the first character of the string as the first character of the abbr
    abbreviation = string[0]

    vowels = 'aeiouAEIOU'
    newString = ''
    # removing vowels and non-alphanumeric characters
    for s in string[1:]:
        if s not in vowels and s.isalnum():
            newString += s

    # retaining only the first 3 characters and adding it to abbr
    for i in range(3):
        if i < len(newString):
            abbreviation += newString[i]

    return abbreviation.lower()
    

def scrape():
    """
    This function is intended only to scrape certain urls.
    Every web page has different HTML structure therefore, this function is only
    intended to scrape "https://www.tgifridays.co.jp/foods/" and "https://www.tgifridays.co.jp/drink/".
    Other web pages will need a different function in order to srape properly
    """
    soup = getContent("https://www.tgifridays.co.jp/foods/")

    # locating the food category menu
    foodDiv = soup.find("div", {"id":"controller"})
    aList = foodDiv.findAll('a')
    
    foodCategory = dict()

    # getting list of food categories
    for a in aList:
        categoryId = a['rel'][0].replace('#','')
        categoryName = a.text.strip()
        foodCategory[categoryId] = categoryName

    for categoryId, categoryName in foodCategory.items():
        catImgUrl = soup.find("a", {"class":"nolink","rel":"#"+categoryId})

        catImgUrl = catImgUrl.img['src']
        categoryName = categoryName.lower()
        categoryAbbr = makeAbbreviation(categoryName)
        
        # saving category
        Category(categoryName, categoryAbbr, 'food', catImgUrl)

        li = soup.find("div", {"id":categoryId})
        liList = li.findAll("li", class_="menu-item")
    
        # getting the list of food under each category
        subCategory = categoryName
        for li in liList:
            if len(li['class']) > 1:
                subCategory = li.text.lower().strip()
                continue
    
            imgUrl = li.img['src']
    
            food = getStrippedString(li.a)
            name = ' '.join(food[:-1])
            tname = food[-1]
    
            details = getStrippedString(li.div.p)
            details = ' '.join(details)
    
            details = details.rsplit('！', 1)
    
            if len(details) == 1:
                details = details[0].rsplit('。', 1)
    
            price = getPrices(details[1]).lower()
    
            # saving item
            Item(name, tname, categoryAbbr, subCategory, 'food', price, imgUrl)
    

    soup = getContent("https://www.tgifridays.co.jp/drinks/")
    
    # locating the drink category menu
    drinkDiv = soup.find("div", {"id":"ultimates"})
    liList = drinkDiv.find_all('li', class_="menu-item")
    
    # getting list of drink categories and translations
    for li in liList:
        categoryName = li.a.contents[0].text.lower().strip()
        categoryAbbr = makeAbbreviation(categoryName)
        
        Category(categoryName, categoryAbbr, 'drink')
    
        pList = li.div.find_all("p")
    
        subCategory = categoryName
        for p in pList:
            if p.has_attr('class'):
                subCategory = p.text.lower().strip()
                continue
            
            drink = getStrippedString(p)

            tname = drink[-1]
            drink = ' '.join(drink[:-1])
    
            price = getPrices(drink).lower()
            drink = drink.split("/")
            name = drink[0].strip()

            # specific string replacement
            # string pattern cannot be recognized
            name = name.replace("（S）550円（税込605円）", "")
    
            Item(name, tname, categoryAbbr, subCategory, 'drink', price)

    return {'items':Item.all,'categories':Category.all}
    