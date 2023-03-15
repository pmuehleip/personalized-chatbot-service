import uuid
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from .dynamodb_client import DynamoDBClient

class ChatDynamoDBClient:
    def __init__(self, table_name: str):
        self.client = DynamoDBClient(table_name)
        self.serializer = TypeSerializer()
        self.deserializer = TypeDeserializer()


    def get_chat(self, id: str):
        key = {
            'id': {'S': id}
        }
        item = self.client.get_item(key=key)
        if not item:
            return None
        
        messages = [self.deserialize(message.get('M')) for message in item.get('messages').get('L')]
        return {'id': item.get('id').get('S'), 'chatbot_id': item.get('chatbot_id').get('S'), 'messages': messages}


    # TODO: Do we still need this?
    # NOTE (HOW TO USE): client.add_chat_messages("123", messages=[{"role": "user", "content": "what is the meaning of life?"}, {"role": "assistant", "content": "47"}])
    def add_chat_messages(self, id: str, messages: list[dict]):
        key = {
            'id': {'S': id}
        }
        update_expression = 'SET #messages = list_append(if_not_exists(#messages, :empty_list), :new_messages)'
        expression_attribute_values = {
            ':new_messages': {'L': [{'M': {"S": self.serialize(m)}} for m in messages]},
            ':empty_list': {'L': []}
        }
        expression_attribute_names = {
            '#messages': 'messages'
        }
        self.client.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )

    # {"role": "", "content": ""}
    # {"role": {"S": ""}, "content": {"S": ""}}
    def update_chat_messages(self, id: str, messages: list[dict]):
        key = {
            'id': {'S': id}
        }
        update_expression = 'SET messages = :new_messages'
        expression_attribute_values = {
            ':new_messages': {'L': [{'M': self.serialize(message)} for message in messages]}
        }

        self.client.update_item(key=key, update_expression=update_expression, expression_attribute_values=expression_attribute_values)


    def create_chat(self, chatbot_id: str):
        id = str(uuid.uuid4())
        item = {
            'id': {'S': id},
            'chatbot_id': {'S': chatbot_id},
        }
        self.client.put_item(item=item)
        return id
    

    def serialize(self, input_dict):
        return {key: self.serializer.serialize(value) for key, value in input_dict.items()}


    def deserialize(self, input_dict):
        return  {key: self.deserializer.deserialize(value) for key, value in input_dict.items()}
