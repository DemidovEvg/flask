from flask_combo_jsonapi import Api
from project.shemas_mapping import PlaceList, PlaceDetail


def register(api: Api):
    api.route(
        PlaceList,
        'place_list_api',
        '/api/places',
        tag="Trucks"
    )
    api.route(
        PlaceDetail,
        'place_detail_api',
        '/api/places/<int:id>',
        tag="Trucks"
    )
