from .dynamodb_client import DynamoDBClient

class UsersDynamoDBClient:
    def __init__(self, table_name):
        self.client = DynamoDBClient(table_name)


    def get_user(self, user_id):
        key = {
            'userId': {'S': user_id}
        }
        item = self.client.get_item(key=key)
        if not item:
            return None
        
        return {'userId': item.get('userId').get('S'), 'name': item.get('name').get('S')}


    def create_user(self, user_id, name):
        item = {
            'userId': {'S': user_id},
            'name': {'S': name},
        }
        self.client.put_item(item=item)