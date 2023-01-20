import datetime as dt
from typing import Any
import sqlalchemy as sa
from sqlalchemy.orm import relationship, Session
from sqlalchemy import func
from sqlalchemy import inspect
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from project.database import db
from project.extensions.security import flask_bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    firstname = sa.Column(sa.String(120),
                          unique=False,
                          nullable=False,
                          default='',
                          server_default='')
    lastname = sa.Column(sa.String(120),
                         unique=False,
                         nullable=False,
                         default='',
                         server_default='')
    username = sa.Column(sa.String(50),
                         unique=False,
                         nullable=False,
                         default='',
                         server_default='')
    email = sa.Column(sa.String(120), unique=True, index=True)
    password = sa.Column(sa.LargeBinary(), nullable=False)
    experience = sa.Column(sa.Integer)
    trucks = relationship('Truck', back_populates='driver')
    is_staff = sa.Column(sa.Boolean, nullable=False, default=False)
    is_superuser = sa.Column(sa.Boolean, nullable=False, default=False)
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'<User {self.username!r}>'

    def __str__(self):
        return self.username

    @classmethod
    def get_user(cls, email: str):
        session: Session = db.session
        currrent_user: User = (session.query(User)
                               .filter(func.lower(User.email) == func.lower(email))
                               .one_or_none())
        return currrent_user

    def set_password(self, value):
        self.password = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        if self.password.decode('utf-8').startswith('sha256$'):
            return check_password_hash(self.password.decode('utf-8'), password)
        return flask_bcrypt.check_password_hash(self.password, password)


class Truck(db.Model):
    __tablename__ = 'trucks'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), unique=True, index=True)
    image_path = sa.Column(sa.String(120), unique=True)
    description = sa.Column(sa.String, unique=False)
    driver = relationship(User, back_populates='trucks')
    driver_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    dt_created = sa.Column(
        sa.DateTime,
        default=dt.datetime.utcnow,
        server_default=func.now(),
        index=True
    )
    dt_updated = sa.Column(
        sa.DateTime,
        default=dt.datetime.utcnow,
        server_default=func.now(),
        index=True
    )
    trips = relationship('Trip', back_populates='truck')

    def __repr__(self):
        return f'<Truck {self.name!r}>'

    def __str__(self):
        return self.name


trip_product_associations_table = sa.Table(
    'trip_product_associations',
    db.metadata,
    sa.Column('trip_id',
              sa.Integer,
              sa.ForeignKey('trip.id'),
              nullable=False),
    sa.Column('product_id',
              sa.Integer,
              sa.ForeignKey('product.id'),
              nullable=False)
)


class Trip(db.Model):
    __tablename__ = 'trip'
    id = sa.Column(sa.Integer, primary_key=True)
    truck_id = sa.Column(sa.Integer, sa.ForeignKey('trucks.id'))
    truck = relationship(
        'Truck',
        back_populates='trips',
        foreign_keys=[truck_id]
    )
    departure_place_id = sa.Column(sa.Integer, sa.ForeignKey('place.id'))
    departure_place = relationship(
        'Place',
        back_populates='trips_from',
        foreign_keys=[departure_place_id]
    )
    arrival_place_id = sa.Column(sa.Integer, sa.ForeignKey('place.id'))
    arrival_place = relationship(
        'Place',
        back_populates='trips_to',
        foreign_keys=[arrival_place_id]
    )
    departure_at = sa.Column(sa.DateTime, nullable=True)
    arrival_at = sa.Column(sa.DateTime, nullable=True)
    products = relationship(
        'Product',
        secondary=trip_product_associations_table,
        back_populates='trips'
    )

    @classmethod
    def filter_fields(cls, fields: dict[str, Any]) -> dict[str, Any]:
        mapper = inspect(cls)

        properties = [p for p in mapper.attrs]
        keys = [p.key for p in properties]
        new_fields = {}
        for name, value in fields.items():
            if name in keys:
                new_fields[name] = value
        return new_fields


class Product(db.Model):
    __tablename__ = 'product'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), unique=True, index=True)
    trips = relationship(
        'Trip',
        secondary=trip_product_associations_table,
        back_populates='products'
    )


class Place(db.Model):
    __tablename__ = 'place'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), unique=True, index=True)
    trips_from = relationship(
        'Trip',
        back_populates='departure_place',
        foreign_keys=[Trip.departure_place_id]
    )
    trips_to = relationship(
        'Trip',
        back_populates='arrival_place',
        foreign_keys=[Trip.arrival_place_id]
    )
