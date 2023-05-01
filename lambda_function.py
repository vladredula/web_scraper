import json
from db import DynamoDB
from scraper import *

def lambda_handler(event, context):
    message = []
    
    scraped_items = scrape()
    
    # check if the tables need for scraping exists
    # if table is found, delete all items in it
    # if not found, make a new table
    
    # for items table
    item_table = DynamoDB()
    
    if (item_table.table_exists('items')):
        item_table.truncate_table()
    else:
        # table name: 'items'
        # primary key: 'id'
        item_table.create_table('items', 'id')
        
    # put all items into table
    for item in scraped_items['items']:
        if not item_table.put_item(item.__dict__):
            message.append('Error putting item: {}.'.format(item.name))
            break


    # for catagories table
    category_table = DynamoDB()
    
    if (category_table.table_exists('categories')):
        category_table.truncate_table()
    else:
        # table name: 'categories'
        # primary key: 'id'
        category_table.create_table('categories', 'id')
    
    for category in scraped_items['categories']:
        if not category_table.put_item(category.__dict__):
            message.append('Error putting category: {}.'.format(category.name))
            break 


    return {
        'statusCode': 500 if message else 200,
        'body': json.dumps(message if message else 'Scraping completed!')
    }