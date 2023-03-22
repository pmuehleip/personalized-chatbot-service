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

    def update_chatbot(self, id: str, role: str = None, greeting: str = None, title: str = None, description: str = None):
        key = {
            'id': {'S': id}
        }
        update_expression = 'SET '
        expression_attribute_values = {}
        expression_attribute_names = {}
        if role:
            update_expression += '#r = :role, '
            expression_attribute_values[':role'] = {'S': role}
            expression_attribute_names['#r'] = 'role'
        if greeting:
            update_expression += 'greeting = :greeting, '
            expression_attribute_values[':greeting'] = {'S': greeting}
        if title:
            update_expression += 'title = :title, '
            expression_attribute_values[':title'] = {'S': title}
        if description:
            update_expression += 'description = :description, '
            expression_attribute_values[':description'] = {'S': description}

        # Remove the trailing comma and space from the update_expression
        update_expression = update_expression[:-2]

        self.client.update_item(key=key, update_expression=update_expression, expression_attribute_values=expression_attribute_values, expression_attribute_names=expression_attribute_names)
