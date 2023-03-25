import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class DynamoDB:
    def __init__(self):
        self.resource = boto3.resource('dynamodb', region_name='ap-northeast-1')
        self.table = None
    
    # Create a new table with the specified name and primary key
    def create_table(self, table_name, primary_key):
        try:
            self.table = self.resource.create_table(
                TableName = table_name,
                KeySchema = [
                    {
                        'AttributeName': primary_key,
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions = [
                    {
                        'AttributeName': primary_key,
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput = {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            self.table.wait_until_exists()
            
        except ClientError as e:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s", table_name,
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise
        else:
            return self.table

    # Add a new item to a DynamoDB table
    def put_item(self, item):
        try:
            self.table.put_item(Item = item)
        except ClientError as e:
            logger.error(
                "Couldn't add item to table %s. Here's why: %s: %s",
                self.table.name,
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise
        
    # Check if table exists in DynamoDB
    def table_exists(self, table_name):
        try:
            table = self.resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    self.table.name,
                    e.response['Error']['Code'], e.response['Error']['Message'])
                raise
        else:
            self.table = table
        return exists
 
    def truncate_table(self):
        # get all items in the table first
        try:
            scan = self.table.scan(
                ProjectionExpression='#k',
                ExpressionAttributeNames = {'#k': 'id'}
            )
        except ClientError as e:
            logger.error(
                "Couldn't scan table %s. Here's why: %s: %s", 
                self.table.name,
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise
        
        # Delete items in batches
        with self.table.batch_writer() as batch:
            for item in scan['Items']:
                try:
                    batch.delete_item(Key = item)
                except ClientError as e:
                    logger.error(
                        "Couldn't delete item in table %s. Here's why: %s: %s", 
                        self.table.name,
                        e.response['Error']['Code'], 
                        e.response['Error']['Message'])
