from bs4 import BeautifulSoup
import requests
from pprint import pprint

url = "https://www.tgifridays.co.jp/foods/"

response = requests.get(url)

content = response.content

soup = BeautifulSoup(content, "html.parser")

# getting the food category menu
food_cat = soup.find("div", {"id":"controller"})

aList = food_cat.findAll('a')

menu = dict()

for a in aList:
    id = a['rel'][0].replace('#','')
    menu[id] = {'name':a.text}


for id in menu.keys():
    li = soup.find("div", {"id":id})
    liList = li.findAll("li", class_="menu-item")

    for li in liList:
        if len(li['class']) > 1:
            continue
        foodname = li.a.text
        japname = li.a.span.text
        foodname = foodname.replace(japname, '')
        fooddesc = li.p.text
        fooddesc = fooddesc.replace(japname, '')
        fooddesc = fooddesc.replace('\n', '')
        menu[id][foodname] = (japname, fooddesc)

print(menu)
exit()

# 0 - name of food
# 1 - japanese name
# 3 - description and price