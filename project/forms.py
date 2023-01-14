import wtforms
from wtforms import validators
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    firstname = wtforms.StringField("Имя")
    lastname = wtforms.StringField("Фамилия")
    username = wtforms.StringField(
        "Логин",
        [validators.DataRequired()],
    )
    email = wtforms.StringField(
        "Почта",
        [
            validators.DataRequired(),
            validators.Email(),
            validators.Length(min=6, max=200),
        ],
        filters=[lambda data: data and data.lower()],
    )
    password = wtforms.PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
            validators.Length(min=3, max=200)
        ],
    )
    confirm = wtforms.PasswordField("Пароль повторно")


class AuthorizationForm(FlaskForm):
    email = wtforms.StringField(
        'Почта',
        [validators.Email('Введите валидную почту')]
    )
    password = wtforms.SearchField(
        'Пароль',
        [
            validators.Length(
                min=3,
                max=25,
                message='Значение должно быть не менее 3 и не более 25 символов')
        ]
    )
