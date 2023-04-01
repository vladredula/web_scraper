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


def get_prices(string):
    string = string.replace("（", "(")
    string = string.replace("）", ")")
    string = string.replace(",", "")
    string = string.replace("グラス", "glass")
    string = string.replace("ボトル", "bottle")
    string = string.replace("ハーフサイズ", "half")
    string = string.replace("レギュラーサイズ", "regular")
    string = string.replace("フルサイズ", "full")
    # strings = string.split("円)")

    patterns = [r"\((\w)\)(\d+)円\(税込(\d+)", 
                r"(\d\w)\ (\d+)円\(税込(\d+)", 
                r"(\w+)\:(\d+)円\(税込(\d+)", 
                r"(\w+)\ (\d+)円\(税込(\d+)", 
                r"(\w+)(\d+)円\(税込(\d+)", 
                r"(\d+)円\(税込(\d+)",
                r"(\d+)円\ \(税込(\d+)"
    ]

    prices = {}
    # for string in strings:
    for pattern in patterns:
        matches = re.findall(pattern, string)
        if matches != None and matches != []:
            for match in matches:
                if len(match) == 2:
                    prices['1'] = match[1]
                else:
                    prices[match[0]] = match[2]
            break
    
    return prices


def make_abbreviation(str):
    if str == '':
        return str
        
    str = str.strip()
    abbreviation = str[0]

    vowels = 'aeiouAEIOU'
    new_str = ''
    for s in str[1:]:
        if s not in vowels and s.isalnum():
            new_str += s

    for i in range(3):
        if i < len(new_str):
            abbreviation += new_str[i]

    return abbreviation.lower()
    

def scrape():
    soup = getContent("https://www.tgifridays.co.jp/foods/")

    # locating the food category menu
    cat_menu = soup.find("div", {"id":"controller"})
    aList = cat_menu.findAll('a')
    
    food_category = dict()

    # getting list of food categories
    for a in aList:
        category_id = a['rel'][0].replace('#','')
        category_name = a.text.strip()
        food_category[category_id] = category_name

    for category_id, category_name in food_category.items():
        cat_img_url = soup.find("a", {"class":"nolink","rel":"#"+category_id})

        cat_img_url = cat_img_url.img['src']
        category_name = category_name.lower()
        category_abbr = make_abbreviation(category_name)
        
        Category(category_name, category_abbr, 'F', cat_img_url)

        li = soup.find("div", {"id":category_id})
        liList = li.findAll("li", class_="menu-item")
    
        # getting the list of food under each category
        sub_cat = ""
        for li in liList:
            if len(li['class']) > 1:
                sub_cat = li.text
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
            price = get_prices(details[1])
    
            Item(name, tname, detail, category_abbr, sub_cat, img, 'F', price)
    

    soup = getContent("https://www.tgifridays.co.jp/drinks/")
    
    # locating the drink category menu
    drink_menu = soup.find("div", {"id":"ultimates"})
    liList = drink_menu.find_all('li', class_="menu-item")
    
    # getting list of drink categories and translations
    for li in liList:
        category_name = li.a.contents[0].text.lower().strip()
        category_abbr = make_abbreviation(category_name)
        
        Category(category_name, category_abbr, 'D')
    
        pList = li.div.find_all("p")
    
        sub_cat = ""
        for p in pList:
            if p.has_attr('class'):
                sub_cat = p.text
                continue
            
            drink = getStrippedString(p)

            tname = drink[-1]
            drink = ' '.join(drink[:-1])
    
            price = get_prices(drink)
            drink = drink.split("/")
            name = drink[0]

            Item(name, tname, '', category_abbr, sub_cat, '', 'D', price)

    for item in Category.all:
        print(item.__dict__)

    for item in Item.all:
        print(item.__dict__)
    exit()
    
scrape()