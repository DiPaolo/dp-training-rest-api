from flask import Flask, make_response
from flask_restful import reqparse, Api

from web_server.resources.todo_item import TodoItemList

parser = reqparse.RequestParser()
parser.add_argument('task')


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(TodoItemList, '/api/todos')

    @app.after_request
    def after_request_func(data):
        response = make_response(data)
        response.headers['Content-Type'] = 'application/json'
        return response

    return app


def start():
    app = create_app()
    return app.run(debug=False, host='0.0.0.0', port=19931)
