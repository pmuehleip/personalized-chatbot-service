from flask import jsonify, make_response, request
from dynamodb_module.users_dynamodb_client import UsersDynamoDBClient
#from .chat_bot_service import ChatBotService

def init_routes(app, users_dynamodb_client: UsersDynamoDBClient, chatBotService):

    @app.route('/users/<string:user_id>')
    def get_user(user_id):
        user = users_dynamodb_client.get_user(user_id=user_id)
        if not user:
            return jsonify({'error': 'Could not find user with provided "userId"'}), 404

        return jsonify(user)


    @app.route('/users', methods=['POST'])
    def create_user():
        user_id = request.json.get('userId')
        name = request.json.get('name')
        if not user_id or not name:
            return jsonify({'error': 'Please provide both "userId" and "name"'}), 400

        users_dynamodb_client.create_user(user_id=user_id, name=name)

        return jsonify({'userId': user_id, 'name': name})


    @app.route('/chat', methods=['POST'])
    def create_chat():
        chatbot_id = request.json.get('chatbot_id')
        if not chatbot_id:
            return jsonify({'error': 'Please provide "chatbot_id"'}), 400

        chat_id = chatBotService.create_chat(chatbot_id=chatbot_id)
        return jsonify({'chat_id': chat_id})

    @app.route('/chat/<string:chat_id>', methods=['POST'])
    def post_chat(chat_id):
        message = request.json.get('message')
        if not message or not chat_id:
            return jsonify({'error': 'Please provide both a "message" and "chat_id"'}), 400

        bot_message = chatBotService(chat_id=chat_id, message=message)
        return jsonify({'bot_message': bot_message})
    

    @app.route('/chat/<string:chat_id>', methods=['GET'])
    def get_chat(chat_id):
        chat = chatBotService.get_chat(chat_id=chat_id)
        if not chat:
            return jsonify({'error': 'Could not get chat with provided "chat_id"'}), 404
        
        messages = chat.get("messages")
        if not messages:
            messages = []

        return jsonify(messages)


    @app.errorhandler(404)
    def resource_not_found(e):
        return make_response(jsonify(error='Not found!'), 404)


    # @app.before_first_request
    # def on_init():
    #     # code to be executed when the application starts up
    #     print("Flask application has started!")