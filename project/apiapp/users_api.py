from flask_combo_jsonapi import Api
from project.shemas_mapping import UserList, UserDetail


def register(api: Api):
    api.route(
        UserList,
        'user_list_api',
        '/api/users',
        tag="Users"
    )
    api.route(
        UserDetail,
        'user_detail_api',
        '/api/users/<int:id>',
        tag="Users"
    )
