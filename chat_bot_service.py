import openai
from dynamodb_module.chat_dynamodb_client import ChatDynamoDBClient

MODEL = "gpt-3.5-turbo-0301"
ROLE = """
Role: you are an expert plumber. You are here to help me with my water heater issues. You ask me a series of questions to understand the issue and determine what the problem is. You only ask me one question at a time, receiving my responses, until you have enough context to make a good assumption. You then tell me the issue.

Note: If you've determined that sediment build-up is the issue, you suggest using the Turbo Tank Cleaner which is a DIY tool for homeowners. This tool is only sold online at turbotankcleaner.com . You never recommend calling a plumber when a customer can use the Turbo Tank Cleaner as it is made for homeowners and is completely safe.
"""
GREETING = "Hello! I'm here to help you with your water heater issues. Can you explain what kind of problems you are experiencing?"


class ChatBotService:

    def __init__(self, chat_dynamodb_client: ChatDynamoDBClient):
        self.chat_dynamodb_client = chat_dynamodb_client
    
    def __call__(self, chat_id, message):
        chat = self.chat_dynamodb_client.get_chat(id=chat_id)
        if not chat:
            return None # TODO: Is this correct behavior? Maybe should throw error and handle higher up.
        
        messages = chat.get("messages")
        if not messages:
            messages = []

        messages.append(self.format_message(role="user", message=message))

        response_message = self.execute(messages=messages)

        messages.append(self.format_message(role="assistant", message=response_message))

        self.chat_dynamodb_client.update_chat_messages(id=chat_id, messages=messages)

        return response_message
    
    def execute(self, messages: list[dict]):
        completion = openai.ChatCompletion.create(model=MODEL, messages=messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        # print(completion.usage)
        print(completion)
        return completion.choices[0].message.content
    
    def create_chat(self, chatbot_id: str):
        role = ROLE # TODO
        greeting = GREETING # TODO
        messages = []
        if role:
            messages.append(self.format_message(role="system", message=role))
        if greeting:
            messages.append(self.format_message(role="assistant", message=greeting))

        chat_id = self.chat_dynamodb_client.create_chat(chatbot_id=chatbot_id)
        self.chat_dynamodb_client.update_chat_messages(id=chat_id, messages=messages)
        return chat_id

    def get_chat(self, chat_id):
        return self.chat_dynamodb_client.get_chat(id=chat_id)

    def format_message(self, role: str, message: str):
        return {"role": role, "content": message}