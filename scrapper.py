from bs4 import BeautifulSoup
import requests
from item import Food, Drink

def getContent(url):
    response = requests.get(url)
    content = response.content
    content = BeautifulSoup(content, "html.parser")
    return content

def getStrippedString(str):
    str = str.stripped_strings
    return list(str)


soup = getContent("https://www.tgifridays.co.jp/foods/")

# locating the food category menu
cat_menu = soup.find("div", {"id":"controller"})
aList = cat_menu.findAll('a')

food_category = dict()

# getting list of food categories
for a in aList:
    id = a['rel'][0].replace('#','')
    category_name = a.text
    food_category[id] = category_name


for id in food_category.keys():
    li = soup.find("div", {"id":id})
    liList = li.findAll("li", class_="menu-item")

    # getting the list of food under each category
    sub_cat = ''
    for li in liList:
        if len(li['class']) > 1:
            sub_cat = li.text
            continue

        food = getStrippedString(li.a)
        name = ' '.join(food[:-1])
        tname = food[-1]

        details = getStrippedString(li.div.p)
        details = ' '.join(details)

        details = details.rsplit('！', 1)

        if len(details) == 1:
            details = details[0].rsplit('。', 1)

        detail = details[0].replace(tname, "")
        price = details[1]

        Food(name, tname, detail, price, food_category[id], sub_cat)


soup = getContent("https://www.tgifridays.co.jp/drinks/")

# locating the drink category menu
drink_cat = soup.find("div", {"id":"ultimates"})
liList = drink_cat.find_all('li', class_="menu-item")

drinks = dict()

# getting list of drink categories and translations
for li in liList:
    category_name = li.a.contents[0]+'/'+li.a.span.text

    drinks[name] = {}

    pList = li.div.find_all("p")

    sub_cat = ''
    for p in pList:
        if p.has_attr('class'):
            sub_cat = p.text
            continue
        
        drink = getStrippedString(p)
        tname = drink[-1]
        drink = ' '.join(drink[:-1])

        drink = drink.split("/")
        name = drink[0]
        price = drink[1]

        Drink(name, tname, '', price, category_name, sub_cat)

for food in Food.all:
    print(food.__dict__)
exit()