import sqlalchemy as sa
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from project.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), unique=True)
    email = sa.Column(sa.String(120), unique=True)
    password = sa.Column(sa.String(100))
    experience = sa.Column(sa.Integer)
    trucks = relationship('Truck', back_populates="driver")
    is_staff = sa.Column(sa.Boolean, nullable=False, default=False)
    is_superuser = sa.Column(sa.Boolean, nullable=False, default=False)
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'<User {self.name!r}>'

    def __str__(self):
        return self.name


class Truck(db.Model):
    __tablename__ = 'trucks'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), unique=True)
    image_path = sa.Column(sa.String(120), unique=True)
    description = sa.Column(sa.String, unique=False)
    driver = relationship(User, back_populates="trucks")
    driver_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    def __repr__(self):
        return f'<Truck {self.name!r}>'

    def __str__(self):
        return self.name
