from flask import Blueprint, jsonify, request

from services import ChatbotService


class ChatbotRouter:

    def __init__(self, chatbotService: ChatbotService):
        self.blueprint = Blueprint('chatbot_router', __name__,)

        @self.blueprint.route('/chatbot', methods=['POST'])
        def create_chatbot():
            role = request.json.get('role')
            greeting = request.json.get('greeting')
            title = request.json.get('title')
            description = request.json.get('description')
            if not role or not greeting or not title:
                return jsonify({'error': 'Please provide both "role" and "greeting" and "title"'}), 400

            chatbot_id = chatbotService.create_chatbot(role=role, greeting=greeting, title=title, description=description)
            return jsonify({'chatbot_id': chatbot_id})
        
        @self.blueprint.route('/chatbot/<string:chatbot_id>', methods=['GET'])
        def get_chatbot(chatbot_id):
            chatbot = chatbotService.get_chatbot(chatbot_id=chatbot_id)
            if not chatbot:
                return jsonify({'error': 'Could not get chatbot with provided "chatbot_id"'}), 404
            
            return jsonify(chatbot)