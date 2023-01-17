from .database import db
from .models import User, Truck
from sqlalchemy.orm import Session
from .serializers import UserSchema, TruckSchema

session: Session = db.session

users = session.query(User).all()
trucks = session.query(Truck).all()

schema = UserSchema()

dump = {
    'email': 'Ivanov0@gmail.com',
    'username': 'Ivanov',
    'trucks': [{'name': 'hyundai', 'description': "Lorem Ipsum is simply  "}],
    'firstname': 'Ivanov',
    'lastname': 'Ivanov', 'id': 2
}
