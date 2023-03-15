from dynamodb import ChatDynamoDBClient, ChatbotDynamoDBClient
import openai

MODEL = "gpt-3.5-turbo-0301"
DEFAULT_ROLE = """Role: you are an expert plumber. You are here to help me with my water heater issues. You ask me a series of questions to understand the issue and determine what the problem is. You only ask me one question at a time, receiving my responses, until you have enough context to make a good assumption. You then tell me the issue.
Note: If you've determined that sediment build-up is the issue, you suggest using the Turbo Tank Cleaner which is a DIY tool for homeowners. This tool is only sold online at turbotankcleaner.com . You never recommend calling a plumber when a customer can use the Turbo Tank Cleaner as it is made for homeowners and is completely safe."""
DEFAULT_GREETING = "Hello! I'm here to help you with your water heater issues. Can you explain what kind of problems you are experiencing?"

def format_message(role: str, message: str):
    return {"role": role, "content": message}

class ChatbotService:

    def __init__(self, chatDynamoDBClient: ChatDynamoDBClient, chatbotDynamoDBClient: ChatbotDynamoDBClient, openaiClient: openai):
        self.chatDynamoDBClient = chatDynamoDBClient
        self.chatbotDynamoDBClient = chatbotDynamoDBClient
        self.openaiClient = openaiClient
    
    def reply(self, chat_id, message):
        chat = self.chatDynamoDBClient.get_chat(id=chat_id)
        if not chat:
            return None # TODO: Is this correct behavior? Maybe should throw error and handle higher up.
        
        messages = chat.get("messages")
        if not messages:
            messages = []

        messages.append(format_message(role="user", message=message))

        response_message = self.do_chat_completion(messages=messages)

        messages.append(format_message(role="assistant", message=response_message))

        self.chatDynamoDBClient.update_chat_messages(id=chat_id, messages=messages)

        return response_message
    
    def do_chat_completion(self, messages: list[dict]):
        completion = self.openaiClient.ChatCompletion.create(model=MODEL, messages=messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        # print(completion.usage)
        print(completion)
        return completion.choices[0].message.content
    
    def create_chat(self, chatbot_id: str):
        chatbot = self.get_chatbot(chatbot_id=chatbot_id)
        role = chatbot.get("role", DEFAULT_ROLE)
        greeting = chatbot.get("greeting", DEFAULT_GREETING)

        messages = []
        if role:
            messages.append(format_message(role="system", message=role))
        if greeting:
            messages.append(format_message(role="assistant", message=greeting))

        chat_id = self.chatDynamoDBClient.create_chat(chatbot_id=chatbot_id)
        self.chatDynamoDBClient.update_chat_messages(id=chat_id, messages=messages)
        return chat_id

    def get_chat(self, chat_id):
        return self.chatDynamoDBClient.get_chat(id=chat_id)

    def create_chatbot(self, role: str, greeting: str):
        return self.chatbotDynamoDBClient.create_chatbot(role=role, greeting=greeting)

    def get_chatbot(self, chatbot_id: str):
        return self.chatbotDynamoDBClient.get_chatbot(id=chatbot_id)
