import flask
from flask import g, redirect, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy.orm import Session
from sqlalchemy import func
from werkzeug.security import check_password_hash
from project.models import User

auth_blueprint = flask.Blueprint(
    name='authapp',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/'
)


@auth_blueprint.route('/login', endpoint='login_view', methods=["GET", "POST"])
def login_view():
    request = flask.request
    next = flask.request.args.get('next')
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        session: Session = g.session
        currrent_user = (session.query(User)
                                .filter(func.lower(User.email) == func.lower(email))
                                .one_or_none())

        if currrent_user and check_password_hash(currrent_user.password, password):
            flask.flash('Enter success', 'alert-success')
            login_user(currrent_user)
            return flask.redirect(next or flask.url_for('start_view'))

        flask.flash('Email or password wrong', 'alert-danger')
        return flask.render_template('authapp/login.html')
    return flask.render_template('authapp/login.html', next=next)


@auth_blueprint.route('/logout', endpoint='logout_view')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for("authapp.login_view"))


@auth_blueprint.route('/profile', endpoint='profile_view')
@login_required
def profile_view():
    return flask.render_template('authapp/profile.html')
