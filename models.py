from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    experience = Column(Integer)
    trucks = relationship('Truck', back_populates="driver")

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'

    def __str__(self):
        return self.name


class Truck(Base):
    __tablename__ = 'trucks'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    image_path = Column(String(120), unique=True)
    description = Column(String(120), unique=False)
    driver = relationship(User, back_populates="trucks")
    driver_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, name=None, image_path=None, description=None):
        self.name = name
        self.image_path = image_path
        self.description = description

    def __repr__(self):
        return f'<Truck {self.name!r}>'

    def __str__(self):
        return self.name
