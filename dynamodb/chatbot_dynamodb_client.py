import uuid
from .dynamodb_client import DynamoDBClient

class ChatbotDynamoDBClient:
    def __init__(self, table_name: str):
        self.client = DynamoDBClient(table_name)

    def create_chatbot(self, role: str, greeting: str, title: str, description: str):
        id = str(uuid.uuid4())
        item = {
            'id': {'S': id},
            'role': {'S': role},
            'greeting': {'S': greeting},
            'title': {'S': title},
            'description': {'S': description},
        }
        self.client.put_item(item=item)
        return id
    
    def get_chatbot(self, id: str):
        key = {
            'id': {'S': id}
        }
        item = self.client.get_item(key=key)
        if not item:
            return None # TODO: is this correct?
        
        return {'id': item.get('id').get('S'), 'role': item.get('role').get('S'), 'greeting': item.get('greeting').get('S'), 'title': item.get('title').get('S'), 'description': item.get('description').get('S')}
