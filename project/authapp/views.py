import flask
from flask import redirect, url_for, request, current_app
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from project.models import User
from project.database import db
from project.forms import AuthorizationForm, RegistrationForm

session: Session = db.session

auth_blueprint = flask.Blueprint(
    name='authapp',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/'
)


@auth_blueprint.route('/login', methods=["GET", "POST"])
def login_view():
    request = flask.request
    next = flask.request.args.get('next')
    form = AuthorizationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        currrent_user = User.get_user(form.email.data)

        if currrent_user and currrent_user.validate_password(form.password.data):
            flask.flash('Enter success', 'alert-success')
            login_user(currrent_user)
            return flask.redirect(next or flask.url_for('start_view'))

        flask.flash('Email or password wrong', 'alert-danger')
        return flask.render_template('authapp/login.html')

    return flask.render_template('authapp/login.html', next=next, form=form)


@auth_blueprint.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for("authapp.login_view"))


@auth_blueprint.route('/profile')
@login_required
def profile_view():
    return flask.render_template('authapp/profile.html')


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register_view():
    current_app.logger.info("Enter to register_view")
    if current_user.is_authenticated:
        return redirect("truckapp.truck_list_view")

    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        current_user_login = User.get_user(form.email.data)
        if current_user_login:
            form.email.errors.append(
                "Пользователь с данной почтой уже существует!"
            )
            return flask.render_template("authapp/register.html", form=form)

        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("truckapp.truck_list_view"))
    return flask.render_template("authapp/register.html", form=form, error=error)
