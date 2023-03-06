from flask_combo_jsonapi import Api
from project.shemas_mapping import TruckList, TruckDetail


def register(api: Api):
    api.route(
        TruckList,
        'truck_list_api',
        '/api/trucks',
        tag="Trucks"
    )
    api.route(
        TruckDetail,
        'truck_detail_api',
        '/api/trucks/<int:id>',
        tag="Trucks"
    )
