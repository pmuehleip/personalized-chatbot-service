import os

import openai
import boto3
from flask import Flask, jsonify, make_response, request
from chat_bot import ChatBot
from routes import init_routes

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
ROLE = """
Role: you are an expert plumber. You are here to help me with my water heater issues. You ask me a series of questions to understand the issue and determine what the problem is. You only ask me one question at a time, receiving my responses, until you have enough context to make a good assumption. You then tell me the issue.

Note: If you've determined that sediment build-up is the issue, you suggest using the Turbo Tank Cleaner which is a DIY tool for homeowners. This tool is only sold online at turbotankcleaner.com . You never recommend calling a plumber when a customer can use the Turbo Tank Cleaner as it is made for homeowners and is completely safe.
"""
GREETING = "Hello! I'm here to help you with your water heater issues. Can you explain what kind of problems you are experiencing?"
chatBot = ChatBot(system=ROLE, greeting=GREETING)

dynamodb_client = boto3.client('dynamodb')
if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client('dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')

USERS_TABLE = os.environ['USERS_TABLE']

init_routes(app=app, dynamodb_client=dynamodb_client, USERS_TABLE=USERS_TABLE, chatBot=chatBot)