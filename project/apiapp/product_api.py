from flask_combo_jsonapi import Api
from project.shemas_mapping import ProductList, ProductDetail


def register(api: Api):
    api.route(
        ProductList,
        'product_list_api',
        '/api/products',
        tag="Trucks"
    )
    api.route(
        ProductDetail,
        'product_detail_api',
        '/api/products/<int:id>',
        tag="Trucks"
    )
