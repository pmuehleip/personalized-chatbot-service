import os

import openai
from flask import Flask
from flask_cors import CORS
from services import ChatbotService
from routes import UsersRouter, ChatRouter, ChatbotRouter
from dynamodb import UsersDynamoDBClient, ChatDynamoDBClient, ChatbotDynamoDBClient

app = Flask(__name__)
CORS(app, origins="*")

openai.api_key = os.getenv("OPENAI_API_KEY")

USERS_TABLE = os.environ['USERS_TABLE']
CHAT_TABLE =  os.environ['CHAT_TABLE']
CHATBOT_TABLE =  os.environ['CHATBOT_TABLE']

usersDynamoDBClient = UsersDynamoDBClient(table_name=USERS_TABLE)
chatDynamoDBClient = ChatDynamoDBClient(table_name=CHAT_TABLE)
chatbotDynamoDBClient = ChatbotDynamoDBClient(table_name=CHATBOT_TABLE)

chatbotService = ChatbotService(chatDynamoDBClient=chatDynamoDBClient, chatbotDynamoDBClient=chatbotDynamoDBClient, openaiClient=openai)

usersRouter = UsersRouter(usersDynamoDBClient=usersDynamoDBClient)
chatRouter = ChatRouter(chatbotService=chatbotService)
chatbotRouter = ChatbotRouter(chatbotService=chatbotService)

app.register_blueprint(usersRouter.blueprint)
app.register_blueprint(chatRouter.blueprint)
app.register_blueprint(chatbotRouter.blueprint)