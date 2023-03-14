from flask import jsonify, make_response, request

def init_routes(app, dynamodb_client, USERS_TABLE, chatBot):

    # @app.route('/users/<string:user_id>')
    # def get_user(user_id):
    #     result = dynamodb_client.get_item(
    #         TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    #     )
    #     item = result.get('Item')
    #     if not item:
    #         return jsonify({'error': 'Could not find user with provided "userId"'}), 404

    #     return jsonify(
    #         {'userId': item.get('userId').get('S'), 'name': item.get('name').get('S')}
    #     )


    # @app.route('/users', methods=['POST'])
    # def create_user():
    #     user_id = request.json.get('userId')
    #     name = request.json.get('name')
    #     if not user_id or not name:
    #         return jsonify({'error': 'Please provide both "userId" and "name"'}), 400

    #     dynamodb_client.put_item(
    #         TableName=USERS_TABLE, Item={'userId': {'S': user_id}, 'name': {'S': name}}
    #     )

    #     return jsonify({'userId': user_id, 'name': name})


    @app.route('/respond', methods=['POST'])
    def respond():
        message = request.json.get('message')
        if not message:
            return jsonify({'error': 'Please provide both a "message"'}), 400

        bot_message = chatBot(message=message)

        return jsonify({'bot_message': bot_message})


    @app.errorhandler(404)
    def resource_not_found(e):
        return make_response(jsonify(error='Not found!'), 404)


    # @app.before_first_request
    # def on_init():
    #     # code to be executed when the application starts up
    #     print("Flask application has started!")