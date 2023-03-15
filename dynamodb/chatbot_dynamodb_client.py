import uuid
from .dynamodb_client import DynamoDBClient

class ChatbotDynamoDBClient:
    def __init__(self, table_name: str):
        self.client = DynamoDBClient(table_name)

    def create_chatbot(self, role: str, greeting: str):
        id = str(uuid.uuid4())
        item = {
            'id': {'S': id},
            'role': {'S': role},
            'greeting': {'S': greeting},
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
        
        return {'id': item.get('id').get('S'), 'role': item.get('role').get('S'), 'greeting': item.get('greeting').get('S')}
