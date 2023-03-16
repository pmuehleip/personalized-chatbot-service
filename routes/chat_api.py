from flask import Blueprint, jsonify, request

from services import ChatbotService

def format_message(role: str, message: str):
    return {"role": role, "content": message}

class ChatRouter:

    def __init__(self, chatbotService: ChatbotService):
        self.blueprint = Blueprint('chat_router', __name__,)

        @self.blueprint.route('/chat', methods=['POST'])
        def create_chat():
            chatbot_id = request.json.get('chatbot_id')
            if not chatbot_id:
                return jsonify({'error': 'Please provide "chatbot_id"'}), 400

            chat_id = chatbotService.create_chat(chatbot_id=chatbot_id)
            return jsonify({'chat_id': chat_id})


        @self.blueprint.route('/chat/<string:chat_id>', methods=['POST'])
        def post_chat(chat_id):
            message = request.json.get('message')
            if not message or not chat_id:
                return jsonify({'error': 'Please provide both a "message" and "chat_id"'}), 400

            bot_message = chatbotService.reply(chat_id=chat_id, message=message)
            return jsonify(format_message(role="assistant", message=bot_message))
        

        @self.blueprint.route('/chat/<string:chat_id>', methods=['GET'])
        def get_chat(chat_id):
            chat = chatbotService.get_chat(chat_id=chat_id)
            if not chat:
                return jsonify({'error': 'Could not get chat with provided "chat_id"'}), 404
            
            messages = chat.get("messages")
            if not messages:
                messages = []

            return jsonify({"messages": messages})