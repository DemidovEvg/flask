
from sqlalchemy.orm import Session
import sqlalchemy as sa
from flask import abort
from flask_combo_jsonapi import ResourceDetail, ResourceList
from combojsonapi.event.resource import EventsResource
from project.models import User, Truck, Place, Product, Trip
from project.database import db
from project.shemas import (
    UserSchemaCombo,
    TruckSchemaCombo,
    TripSchemaCombo,
    PlaceSchemaCombo,
    ProductSchemaCombo
)
from project.permissions import IsAuthenticatedPermission


session: Session = db.session


base_data_layer = {
    'session': session,
    'permission_get': [IsAuthenticatedPermission],
    'permission_patch': [IsAuthenticatedPermission],
    'permission_post': [IsAuthenticatedPermission],
    'permission_delete': [IsAuthenticatedPermission]
}


class UserList(ResourceList):
    data_layer = dict(model=User)
    data_layer.update(base_data_layer)
    schema = UserSchemaCombo


class UserDetail(ResourceDetail):
    schema = UserSchemaCombo
    data_layer = dict(model=User)
    data_layer.update(base_data_layer)


class TruckList(ResourceList):
    schema = TruckSchemaCombo
    data_layer = dict(model=Truck)
    data_layer.update(base_data_layer)


class TruckDetail(ResourceDetail):
    schema = TruckSchemaCombo
    data_layer = dict(model=Truck)
    data_layer.update(base_data_layer)


class TripList(ResourceList):
    schema = TripSchemaCombo
    data_layer = dict(model=Trip)
    data_layer.update(base_data_layer)


class TripDetail(ResourceDetail):
    schema = TripSchemaCombo
    data_layer = dict(model=Trip)
    data_layer.update(base_data_layer)


class ProductListEvents(EventsResource):
    def event_get_most_popular_product(self):
        products = (
            session.query(Product,
                          sa.func.count(Trip.id).label('trips_count'))
            .join(Product.trips)
            .group_by(Product.id)
            .order_by(sa.desc(sa.func.count(Trip.id).label('trips_count')))
            .all()
        )
        if products:
            return {'most_popular_product': products[0][0].name}
        else:
            raise abort(404)


class ProductList(ResourceList):
    events = ProductListEvents
    schema = ProductSchemaCombo
    data_layer = dict(model=Product)
    data_layer.update(base_data_layer)


class ProductDetail(ResourceDetail):
    schema = ProductSchemaCombo
    data_layer = dict(model=Product)
    data_layer.update(base_data_layer)


class PlaceList(ResourceList):
    schema = PlaceSchemaCombo
    data_layer = dict(model=Place)
    data_layer.update(base_data_layer)


class PlaceDetail(ResourceDetail):
    schema = PlaceSchemaCombo
    data_layer = dict(model=Place)
    data_layer.update(base_data_layer)
