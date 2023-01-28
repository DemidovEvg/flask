
from sqlalchemy.orm import Session
from flask_combo_jsonapi import ResourceDetail, ResourceList
from project.models import User, Truck, Place, Product, Trip
from project.database import db
from project.shemas import (
    UserSchemaCombo,
    TruckSchemaCombo,
    TripSchemaCombo,
    PlaceSchemaCombo,
    ProductSchemaCombo
)


session: Session = db.session


class UserList(ResourceList):
    schema = UserSchemaCombo
    data_layer = {
        'session': session,
        'model': User
    }


class UserDetail(ResourceDetail):
    schema = UserSchemaCombo
    data_layer = {
        'session': session,
        'model': User
    }


class TruckList(ResourceList):
    schema = TruckSchemaCombo
    data_layer = {
        'session': session,
        'model': Truck
    }


class TruckDetail(ResourceDetail):
    schema = TruckSchemaCombo
    data_layer = {
        'session': session,
        'model': Truck
    }


class TripList(ResourceList):
    schema = TripSchemaCombo
    data_layer = {
        'session': session,
        'model': Trip
    }


class TripDetail(ResourceDetail):
    schema = TripSchemaCombo
    data_layer = {
        'session': session,
        'model': Trip
    }


class ProductList(ResourceList):
    schema = ProductSchemaCombo
    data_layer = {
        'session': session,
        'model': Product
    }


class ProductDetail(ResourceDetail):
    schema = ProductSchemaCombo
    data_layer = {
        'session': session,
        'model': Product
    }


class PlaceList(ResourceList):
    schema = PlaceSchemaCombo
    data_layer = {
        'session': session,
        'model': Place
    }


class PlaceDetail(ResourceDetail):
    schema = PlaceSchemaCombo
    data_layer = {
        'session': session,
        'model': Place
    }
