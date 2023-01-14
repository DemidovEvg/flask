import sqlalchemy as sa
from sqlalchemy.orm import relationship, Session
from sqlalchemy import func
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
                          default="",
                          server_default="")
    lastname = sa.Column(sa.String(120),
                         unique=False,
                         nullable=False,
                         default="",
                         server_default="")
    username = sa.Column(sa.String(50),
                         unique=False,
                         nullable=False,
                         default="",
                         server_default="")
    email = sa.Column(sa.String(120), unique=True)
    password = sa.Column(sa.LargeBinary(), nullable=False)
    experience = sa.Column(sa.Integer)
    trucks = relationship('Truck', back_populates="driver")
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
    name = sa.Column(sa.String(50), unique=True)
    image_path = sa.Column(sa.String(120), unique=True)
    description = sa.Column(sa.String, unique=False)
    driver = relationship(User, back_populates="trucks")
    driver_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    def __repr__(self):
        return f'<Truck {self.name!r}>'

    def __str__(self):
        return self.name
