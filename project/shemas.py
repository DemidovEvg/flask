from marshmallow import fields
from flask_marshmallow import fields as flask_marshmallow_fields
import marshmallow_jsonapi
from combojsonapi.utils import Relationship as combojsonapiRelationship


def get_base_schema(name):
    class BaseSchema(marshmallow_jsonapi.Schema):
        class Meta:
            type_ = name
            self_view = f'{name}_detail_api'
            self_view_kwargs = {'id': '<id>'}
            self_view_many = f'{name}_list_api'
    return BaseSchema


class UserSchemaCombo(get_base_schema('user')):
    id = fields.Integer()
    firstname = fields.String()
    lastname = fields.String()
    username = fields.String()
    email = fields.String()
    experience = fields.Integer()
    trucks = flask_marshmallow_fields.Hyperlinks({
        'truck': flask_marshmallow_fields.URLFor('truck_detail_api', values=dict(id='<id>')),
    })


class TruckSchemaCombo(get_base_schema('truck')):
    id = fields.Integer()
    name = fields.String()
    image_path = fields.String()
    description = fields.String()
    dt_created = fields.DateTime()
    dt_updated = fields.DateTime()
    driver = flask_marshmallow_fields.Hyperlinks({
        'driver': flask_marshmallow_fields.URLFor('user_detail_api', values=dict(id='<id>')),
    })


class TripSchemaCombo(get_base_schema('trip')):
    id = fields.Integer()
    truck = combojsonapiRelationship(
        nested="TruckSchemaCombo",
        attribute="truck",
        related_view="truck_detail_api",
        related_view_kwargs={"id": "<id>"},
        schema="TruckSchemaCombo",
        type_="truck",
        many=False,
    )
    departure_place = combojsonapiRelationship(
        nested="PlaceSchemaCombo",
        attribute="departure_place",
        related_view="place_detail_api",
        related_view_kwargs={"id": "<id>"},
        schema="PlaceSchemaCombo",
        type_="place",
        many=False,
    )
    arrival_place = combojsonapiRelationship(
        nested="PlaceSchemaCombo",
        attribute="arrival_place",
        related_view="place_detail_api",
        related_view_kwargs={"id": "<id>"},
        schema="PlaceSchemaCombo",
        type_="place",
        many=False,
    )
    departure_at = fields.DateTime()
    arrival_at = fields.DateTime()
    products = combojsonapiRelationship(
        nested="ProductSchemaCombo",
        attribute="products",
        related_view="product_detail_api",
        related_view_kwargs={"id": "<id>"},
        schema="ProductSchemaCombo",
        type_="product",
        many=True,
    )


class ProductSchemaCombo(get_base_schema('product')):
    id = fields.Integer()
    name = fields.String()
    trips = flask_marshmallow_fields.Hyperlinks({
        'trip': flask_marshmallow_fields.URLFor('trip_detail_api', values=dict(id='<id>')),
    })


class PlaceSchemaCombo(get_base_schema('place')):
    id = fields.Integer()
    name = fields.String()
    trips = flask_marshmallow_fields.Hyperlinks({
        'trip': flask_marshmallow_fields.URLFor('trip_detail_api', values=dict(id='<id>')),
    })
