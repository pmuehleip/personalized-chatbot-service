import os

import openai
import boto3
from flask import Flask, jsonify, make_response, request
from chat_bot_service import ChatBotService
from routes import init_routes
from dynamodb_module.users_dynamodb_client import UsersDynamoDBClient
from dynamodb_module.chat_dynamodb_client import ChatDynamoDBClient

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

USERS_TABLE = os.environ['USERS_TABLE']
CHAT_TABLE =  os.environ['CHAT_TABLE'] # TODO: We need to add env variable.
users_dynamodb_client = UsersDynamoDBClient(table_name=USERS_TABLE)
chat_dynamodb_client = ChatDynamoDBClient(table_name=CHAT_TABLE)

chatBotService = ChatBotService(chat_dynamodb_client=chat_dynamodb_client)

init_routes(app=app, users_dynamodb_client=users_dynamodb_client, chatBotService=chatBotService)


# TODO: Need to add Chat table to serverless.yml file.