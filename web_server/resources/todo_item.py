from flask import request
from flask_restful import Resource, marshal_with, fields, abort, marshal

from web_server import domain, repository

todo_item_fields = {
    'title': fields.String,
    'desc': fields.String,
    'createdAt': fields.DateTime,
    'dueTo': fields.DateTime
}

todo_item_list_fields = {
    'list': fields.List(fields.Nested(todo_item_fields))
}


class TodoItemList(Resource):
    # def __init__(self, data: Dict):

    @marshal_with(todo_item_list_fields)
    def get(self):
        try:
            args = request.args
            req_days = args.get('days', default=3, type=int)
            if req_days < 1 or req_days > 14:
                abort(400, message="Invalid parameter 'days' (must be in range [1, 14])")

            return {
                'list': [i.to_dict() for i in repository.get_todo_items()]
            }
        except Exception as ex:
            abort(500, message=f'Internal error: {type(ex).__name__}: {ex}')

    @marshal_with(todo_item_fields)
    def post(self):
        try:
            if not request.is_json:
                abort(400, message="Invalid or missed input data")

            try:
                in_data = marshal(request.json, todo_item_fields)
                new_item = domain.TodoItem(in_data)
            except:
                abort(400, message="Invalid input data structure")

            repository.add_todo_item(new_item)

            return new_item.to_dict()
        except Exception as ex:
            abort(500, message=f'Internal server error: {type(ex).__name__}: {ex}')
