import sqlalchemy as db
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from project.database import Base


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    trucks = relationship('Truck', back_populates="driver")
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, name, email, password, experience=0):
        self.name = name
        self.email = email
        self.password = password
        self.experience = experience

    def __repr__(self):
        return f'<User {self.name!r}>'

    def __str__(self):
        return self.name


class Truck(Base):
    __tablename__ = 'trucks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    image_path = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(120), unique=False)
    driver = relationship(User, back_populates="trucks")
    driver_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, name, image_path=None, description=None, driver_id=None):
        self.name = name
        self.image_path = image_path
        self.description = description
        self.driver_id = driver_id

    def __repr__(self):
        return f'<Truck {self.name!r}>'

    def __str__(self):
        return self.name
