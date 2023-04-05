from bs4 import BeautifulSoup
import requests
import re
from item import Item
from category import Category
import pprint

def getContent(url):
    response = requests.get(url)
    content = response.content
    content = BeautifulSoup(content, "html.parser")
    
    return content


def getStrippedString(string):
    string = string.stripped_strings
    
    return list(string)


def getPrices(string):
    string = string.replace("（", "(")
    string = string.replace("）", ")")
    string = string.replace(",", "")
    string = string.replace("グラス", "glass")
    string = string.replace("ハーフボトル", "halfbottle")
    string = string.replace("ボトル", "bottle")
    string = string.replace("ハーフサイズ", "half")
    string = string.replace("レギュラーサイズ", "regular")
    string = string.replace("フルサイズ", "full")
    # strings = string.split("円)")

    patterns = [r"\((\w)\)(\d+)円\(税込(\d+)", 
                r"(\d\w)\ (\d+)円\(税込(\d+)", 
                r"(\w+)\:(\d+)円\(税込(\d+)", 
                r"(\w+)\ (\d+)円\(税込(\d+)", 
                r"([a-z]+)([0-9]+)円\(税込(\d+)", 
                r"(\d+)円\(税込(\d+)",
                r"(\d+)円\ \(税込(\d+)"
    ]

    prices = []
    # for string in strings:
    for pattern in patterns:
        matches = re.findall(pattern, string)
        if matches != None and matches != []:
            for match in matches:
                if len(match) == 2:
                    prices.append("1:"+match[1])
                else:
                    prices.append(match[0]+":"+match[2])
            break
    
    return ",".join(prices)


def makeAbbreviation(string):
    if string == '':
        return string
        
    string = string.strip()
    abbreviation = string[0]

    vowels = 'aeiouAEIOU'
    newString = ''
    for s in string[1:]:
        if s not in vowels and s.isalnum():
            newString += s

    for i in range(3):
        if i < len(newString):
            abbreviation += newString[i]

    return abbreviation.lower()
    

def scrape():
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
        
        Category(categoryName, categoryAbbr, 'F', catImgUrl)

        li = soup.find("div", {"id":categoryId})
        liList = li.findAll("li", class_="menu-item")
    
        # getting the list of food under each category
        subCategory = ""
        for li in liList:
            if len(li['class']) > 1:
                subCategory = li.text
                continue
    
            img = li.img['src']
    
            food = getStrippedString(li.a)
            name = ' '.join(food[:-1])
            tname = food[-1]
    
            details = getStrippedString(li.div.p)
            details = ' '.join(details)
    
            details = details.rsplit('！', 1)
    
            if len(details) == 1:
                details = details[0].rsplit('。', 1)
    
            detail = details[0].replace(tname, "")
            price = getPrices(details[1])
    
            Item(name, tname, detail, categoryAbbr, subCategory, img, 'F', price)
    

    soup = getContent("https://www.tgifridays.co.jp/drinks/")
    
    # locating the drink category menu
    drinkDiv = soup.find("div", {"id":"ultimates"})
    liList = drinkDiv.find_all('li', class_="menu-item")
    
    # getting list of drink categories and translations
    for li in liList:
        categoryName = li.a.contents[0].text.lower().strip()
        categoryAbbr = makeAbbreviation(categoryName)
        
        Category(categoryName, categoryAbbr, 'D')
    
        pList = li.div.find_all("p")
    
        subCategory = ""
        for p in pList:
            if p.has_attr('class'):
                subCategory = p.text
                continue
            
            drink = getStrippedString(p)

            tname = drink[-1]
            drink = ' '.join(drink[:-1])
    
            price = getPrices(drink)
            drink = drink.split("/")
            name = drink[0]

            name = name.replace("（S）550円（税込605円）", "")
    
            Item(name, tname, '', categoryAbbr, subCategory, '', 'D', price)

    for item in Category.all:
        print(item.__dict__)

    for item in Item.all:
        print(item.__dict__)
    exit()
    
scrape()