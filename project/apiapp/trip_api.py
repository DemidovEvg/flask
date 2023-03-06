from flask_combo_jsonapi import Api
from project.shemas_mapping import TripList, TripDetail


def register(api: Api):
    api.route(
        TripList,
        'trip_list_api',
        '/api/trips',
        tag="Trucks"
    )
    api.route(
        TripDetail,
        'trip_detail_api',
        '/api/trips/<int:id>',
        tag="Trucks"
    )
