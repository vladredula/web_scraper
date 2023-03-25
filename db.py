import boto3

class DynamoDB:
    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.resource = boto3.resource('dynamodb')
    
    # Create a new table with the specified name and primary key
    def create_table(self, table_name, primary_key):
        response = self.client.create_table(
            TableName = table_name,
            KeySchema = [
                {
                    'AttributeName': primary_key,
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': primary_key,
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        return response

    # Add a new item to a DynamoDB table
    def put_item(self, table_name, item):
        table = self.get_table_resource(table_name)
        response = table.put_item(Item = item)
        return response
        
    # Check if table exists in DynamoDB
    def table_exists(self, table_name):
        response = self.client.list_tables()
        if table_name in response['TableNames']:
            return True
        else:
            return False

 
    def truncate_table(self, table_name):
        table = self.get_table_resource(table_name)
        
        scan = table.scan(
            ProjectionExpression='#k',
            ExpressionAttributeNames={
                '#k': 'id'
            }
        )
        
        with table.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(Key=each)
                
    def get_table_resource(self, table_name):
        table = self.resource.Table(table_name)
        
        return table
