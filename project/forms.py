import datetime as dt
import wtforms as fields
from wtforms import validators, ValidationError
from wtforms.fields.core import widgets
from flask_wtf import FlaskForm
from flask import current_app
from sqlalchemy.orm import Session
from project.database import db
from project.models import Truck, Place, Product, Trip

session: Session = db.session


class RegistrationForm(FlaskForm):
    firstname = fields.StringField("Имя")
    lastname = fields.StringField("Фамилия")
    username = fields.StringField(
        "Логин",
        [validators.DataRequired()],
    )
    email = fields.StringField(
        "Почта",
        [
            validators.DataRequired(),
            validators.Email(),
            validators.Length(min=6, max=200),
        ],
        filters=[lambda data: data and data.lower()],
    )
    password = fields.PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
            validators.Length(min=3, max=200)
        ],
    )
    confirm = fields.PasswordField("Пароль повторно")


class AuthorizationForm(FlaskForm):
    email = fields.StringField(
        'Почта',
        [validators.Email('Введите валидную почту')]
    )
    password = fields.SearchField(
        'Пароль',
        [
            validators.Length(
                min=3,
                max=25,
                message='Значение должно быть не менее 3 и не более 25 символов')
        ]
    )


class DateTimeLocalInput(widgets.DateTimeInput):
    input_type = "datetime-local"
    validation_attrs = ["required", "max", "min", "step"]


class TripForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_form()

    truck_id = fields.SelectField(
        label='Грузовик',
        coerce=int,
        validators=[validators.InputRequired()]
    )
    departure_place_id = fields.SelectField(
        label='Пункт отправления',
        coerce=int,
        validators=[validators.InputRequired()]
    )
    departure_at = fields.DateTimeField(
        label='Дата/время отправления',
        format="%Y-%m-%dT%H:%M",
        widget=DateTimeLocalInput(),
        validators=[validators.DataRequired()]
    )
    arrival_place_id = fields.SelectField(
        label='Пункт прибытия',
        coerce=int,
        validators=[validators.InputRequired()]
    )
    arrival_at = fields.DateTimeField(
        label='Дата/время прибытия',
        format="%Y-%m-%dT%H:%M",
        widget=DateTimeLocalInput(),
        validators=[validators.DataRequired()]
    )
    product_id = fields.SelectField(
        label='Товар',
        coerce=int,
        validators=[validators.InputRequired()]
    )

    def init_form(self):
        trucks: list[Truck] = session.query(Truck).all()
        self.truck_id.choices = [(t.id, t.name) for t in trucks]

        places: list[Place] = session.query(Place).all()
        self.departure_place_id.choices = [(p.id, p.name) for p in places]
        self.arrival_place_id.choices = self.departure_place_id.choices

        products: list[Product] = session.query(Product).all()
        self.product_id.choices = [(p.id, p.name) for p in products]

    @staticmethod
    def validate_departure_at_arrival_at(
        departure_at: dt.datetime,
        arrival_at: dt.datetime
    ):
        if arrival_at < departure_at:
            raise ValidationError(
                'Время отправления не может быть больше времени прибытия'
            )

    @staticmethod
    def validate_departure_place_arrival_place(
        departure_place_id: int,
        arrival_place_id: int
    ):
        if departure_place_id == arrival_place_id:
            raise ValidationError(
                'Нельзя указать одно и тоже место как отправление и прибытие'
            )

    def validate_departure_at(self, *args, **kwargs):
        self.__class__.validate_departure_at_arrival_at(
            self.departure_at.data,
            self.arrival_at.data
        )

    def validate_arrival_at(self, *args, **kwargs):
        self.__class__.validate_departure_at_arrival_at(
            self.departure_at.data,
            self.arrival_at.data
        )

    def validate_departure_place_id(self, *args, **kwargs):
        self.__class__.validate_departure_place_arrival_place(
            self.departure_place_id.data,
            self.arrival_place_id.data
        )

    def validate_arrival_place_id(self, *args, **kwargs):
        self.__class__.validate_departure_place_arrival_place(
            self.departure_place_id.data,
            self.arrival_place_id.data
        )

    def save(self, *args, **kwargs):
        data = {}
        for name, field in self._fields.items():
            data[name] = field.data
        data = Trip.filter_fields(data)
        current_trip = Trip(**data)
        session.add(current_trip)
        session.commit()
        return current_trip
