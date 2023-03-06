from flask_combo_jsonapi import Api
from combojsonapi.spec import ApiSpecPlugin
from combojsonapi.event import EventPlugin
from combojsonapi.permission import PermissionPlugin
from . import users_api
from . import truck_api
from . import place_api
from . import product_api
from . import trip_api


def create_api_spec_plugin(app):
    api_spec_plugin = ApiSpecPlugin(
        app=app,
        tags={
            "Users": "Users API",
            "Trucks": "Trucs API"
        }
    )
    return api_spec_plugin


def init_api(app):
    event_plugin = EventPlugin()
    api_spec_plugin = create_api_spec_plugin(app)
    permission_plugin = PermissionPlugin()
    api = Api(
        app,
        plugins=[
            event_plugin,
            api_spec_plugin,
            permission_plugin
        ]
    )
    users_api.register(api)
    truck_api.register(api)
    trip_api.register(api)
    product_api.register(api)
    place_api.register(api)
