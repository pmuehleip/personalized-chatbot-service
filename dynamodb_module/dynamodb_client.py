import os
import boto3

class DynamoDBClient:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb')
        if os.environ.get('IS_OFFLINE'):
            self.client = boto3.client('dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
        self.table_name = table_name

    def put_item(self, item):
        self.client.put_item(TableName=self.table_name, Item=item)

    def update_item(self, key, update_expression, expression_attribute_values=None, expression_attribute_names=None):
        kwargs = {
            'TableName': self.table_name,
            'Key': key,
            'UpdateExpression': update_expression
        }
        if expression_attribute_values:
            kwargs['ExpressionAttributeValues'] = expression_attribute_values
        if expression_attribute_names:
            kwargs['ExpressionAttributeNames'] = expression_attribute_names
        self.client.update_item(**kwargs)

    def get_item(self, key):
        response = self.client.get_item(TableName=self.table_name, Key=key)
        return response.get('Item', None)

    def delete_item(self, key):
        self.client.delete_item(TableName=self.table_name, Key=key)

    def scan(self, filter_expression=None, expression_attribute_values=None):
        kwargs = {'TableName': self.table_name}
        if filter_expression:
            kwargs['FilterExpression'] = filter_expression
        if expression_attribute_values:
            kwargs['ExpressionAttributeValues'] = expression_attribute_values
        response = self.client.scan(**kwargs)
        return response.get('Items', [])
