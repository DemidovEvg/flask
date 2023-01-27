from marshmallow import fields
from flask_marshmallow import Marshmallow
from project.models import User, Truck


ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = [
            'firstname',
            'lastname',
            'username',
            'email',
            'experience',
            'trucks'
        ]
    trucks = ma.List(ma.HyperlinkRelated("truckapp.truck_detail_api"))


class TruckSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Truck
        fields = [
            'name',
            'description',
            'driver'
        ]
    driver = fields.Nested(UserSchema)
