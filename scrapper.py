from bs4 import BeautifulSoup
import requests
import re
from item import Food, Drink

def getContent(url):
    response = requests.get(url)
    content = response.content
    content = BeautifulSoup(content, "html.parser")
    return content


def getStrippedString(str):
    str = str.stripped_strings
    return list(str)

def extract_price(str):
    str = ''.join(c for c in str if c.isalnum())
    integers = re.findall(r'\d+', str)

    price = []

    for i in integers:
        price.append(int(i))

    return price[1]

def make_abbreviation(str):
    if str == None:
        return None
    
    abbreviation = str[0]

    vowels = 'AEIOU'
    new_str = ''
    for s in str[1:]:
        if s not in vowels and s.isalnum():
            new_str += s

    for i in range(3):
        if i < len(new_str):
            abbreviation += new_str[i]

    return abbreviation.upper()


soup = getContent("https://www.tgifridays.co.jp/foods/")

# locating the food category menu
cat_menu = soup.find("div", {"id":"controller"})
aList = cat_menu.findAll('a')

food_category = dict()

# getting list of food categories
for a in aList:
    id = a['rel'][0].replace('#','')
    category_name = a.text
    food_category[category_name] = id


for category_name, id in food_category.items():
    li = soup.find("div", {"id":id})
    liList = li.findAll("li", class_="menu-item")

    # getting the list of food under each category
    food_category[category_name] = []
    sub_cat = None
    for li in liList:
        if len(li['class']) > 1:
            sub_cat = li.text
            food_category[category_name].append(sub_cat)
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
        price = extract_price(details[1])

        category_id = make_abbreviation(category_name)
        sub_cat_id = make_abbreviation(sub_cat)

        Food(name, tname, detail, price, category_id, sub_cat_id)


soup = getContent("https://www.tgifridays.co.jp/drinks/")

# locating the drink category menu
drink_menu = soup.find("div", {"id":"ultimates"})
liList = drink_menu.find_all('li', class_="menu-item")

drink_category = dict()

# getting list of drink categories and translations
for li in liList:
    category_name = li.a.contents[0] # +'/'+li.a.span.text

    drink_category[category_name] = []

    pList = li.div.find_all("p")

    sub_cat = None
    for p in pList:
        if p.has_attr('class'):
            sub_cat = p.text
            drink_category[category_name].append(sub_cat)
            continue
        
        drink = getStrippedString(p)
        tname = drink[-1]
        drink = ' '.join(drink[:-1])

        drink = drink.split("/")
        name = drink[0]
        price = extract_price(drink[1])

        category_id = make_abbreviation(category_name)
        sub_cat_id = make_abbreviation(sub_cat)

        Drink(name, tname, '', price, category_id, sub_cat_id)



exit()