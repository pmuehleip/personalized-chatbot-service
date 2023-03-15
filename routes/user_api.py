from flask import Blueprint, jsonify, request
from dynamodb import UsersDynamoDBClient



class UsersRouter:

    def __init__(self, usersDynamoDBClient: UsersDynamoDBClient):
        self.blueprint = Blueprint('users_router', __name__,)

        @self.blueprint.route('/users/<string:user_id>')
        def get_user(user_id):
            user = usersDynamoDBClient.get_user(user_id=user_id)
            if not user:
                return jsonify({'error': 'Could not find user with provided "userId"'}), 404

            return jsonify(user)


        @self.blueprint.route('/users', methods=['POST'])
        def create_user():
            user_id = request.json.get('userId')
            name = request.json.get('name')
            if not user_id or not name:
                return jsonify({'error': 'Please provide both "userId" and "name"'}), 400

            usersDynamoDBClient.create_user(user_id=user_id, name=name)

            return jsonify({'userId': user_id, 'name': name})