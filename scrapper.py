from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint

def getContent(url):
    response = requests.get(url)
    content = response.content
    content = BeautifulSoup(content, "html.parser")
    return content

soup = getContent("https://www.tgifridays.co.jp/foods/")

food_cat = soup.find("div", {"id":"controller"})
aList = food_cat.findAll('a')

food = dict()

for a in aList:
    id = a['rel'][0].replace('#','')
    food[id] = {'name':a.text}


for id in food.keys():
    li = soup.find("div", {"id":id})
    liList = li.findAll("li", class_="menu-item")

    for li in liList:
        if len(li['class']) > 1:
            continue
        foodname = li.a.text
        japname = li.a.span.text
        
        foodname = foodname.replace(japname, '')
        japname = japname.replace(' ', '')

        details = li.p.text
        details = details.replace(' ', '')
        details = details.replace(japname, '')
        details = details.replace('\n', '')
        
        details = details.rsplit('。', 1)

        if len(details) == 1:
            details = details[0].rsplit('！', 1)
        
        print(details)
        
        food[id][foodname] = (japname, details[0], details[1])

pprint(food)
exit()

# 0 - name of food
# 1 - japanese name
# 3 - description and price