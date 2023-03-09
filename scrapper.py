from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint

def getContent(url):
    response = requests.get(url)
    content = response.content
    content = BeautifulSoup(content, "lxml")
    return content

def getStrippedString(str):
    str = str.stripped_strings
    return list(str)

def getDrink(str):
    drink = getStrippedString(str)
    tname = drink[-1]
    del(drink[-1])

    drink = ' '.join(drink)
    drink = drink.split("/")
    ename = drink[0]+"/"+tname
    price = drink[1]
    return [ename, price]

def getFood(str):
    return

soup = getContent("https://www.tgifridays.co.jp/drinks/")

# locating the drink category menu
drink_cat = soup.find("div", {"id":"ultimates"})
liList = drink_cat.find_all('li', class_="menu-item")

drinks = dict()

# getting list of drink categories and translations
for li in liList:
    ename = li.a.contents[0]
    tname = li.a.span.text
    name = ename+"/"+tname

    drinks[name] = {}

    pList = li.div.find_all("p", class_="group")

    if len(pList) > 0:
        # getting sub categories for drinks
        for p in pList:
            div = p.find_next_sibling("div")

            # getting the drinks under the subcategory
            dList = []
            for p1 in div.find_all("p"):
                dList.append(getDrink(p1))

            drinks[name][p.text] = dList
    else:
        dList = []
        for p1 in li.div.div.find_all("p"):
            dList.append(getDrink(p1))

        drinks[name] = dList

soup = getContent("https://www.tgifridays.co.jp/foods/")

# locating the food category menu
food_cat = soup.find("div", {"id":"controller"})
aList = food_cat.findAll('a')

foods = dict()
foodIds = dict()

# getting list of food categories
for a in aList:
    id = a['rel'][0].replace('#','')
    foodcat = a.text
    foodIds[id] = foodcat


for id in foodIds.keys():
    li = soup.find("div", {"id":id})
    liList = li.findAll("li", class_="menu-item")

    # getting the list of food under each category
    fList = []
    for li in liList:
        if len(li['class']) > 1:
            continue

        food = getStrippedString(li.a)
        tname = food[-1]
        del(food[-1])

        food = ' '.join(food)
        ename = food+"/"+tname
        
        details = getStrippedString(li.div.p)
        details = ' '.join(details)

        details = details.rsplit('！', 1)

        if len(details) == 1:
            details = details[0].rsplit('。', 1)

        detail = details[0].replace(tname, "")
        detail = detail.strip()
        price = details[1].strip()
        
        fList.append([ename, detail, price])
        
    foods[foodIds[id]] = fList

pprint(foods)
exit()

# 0 - name of food
# 1 - japanese name
# 3 - description and price