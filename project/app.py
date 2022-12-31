import os

from flask import Flask, redirect, url_for, g
from flask_login import LoginManager
from sqlalchemy.orm import Session
from project.database import Database
from project.models import User
from project.userapp.views import user_blueprint
from project.truckapp.views import truck_blueprint
from project.authapp.views import auth_blueprint
from project.commands import register_commands


def attach_login_manager(func):
    def inner(*args, **kwargs):
        app = func(*args, **kwargs)
        login_manager = LoginManager()
        login_manager.init_app(app)

        login_manager.login_message = "Please authorize for enter page"
        login_manager.login_message_category = "alert-info"
        login_manager.login_view = "authapp.login_view"

        @login_manager.user_loader
        def load_user(user_id):
            session: Session = g.session
            return session.query(User).filter_by(id=user_id).one()

        return app
    return inner


@attach_login_manager
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    # print(f'{app.instance_path=}')
    # print(f'{app.config=}')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def stick_session():
        db = Database()
        session = db.db_session
        g.session = session

    @app.route('/')
    def start_view():
        return redirect(url_for('userapp.user_list_view'), 301)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(truck_blueprint)
    app.register_blueprint(auth_blueprint)

    register_commands(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return 'Не нашли что хотели'

    return app


# Пригодится на будущее
# @app.route('/')
# @app.route('/counter/start', methods=['GET', 'POST'])
# def start_view():
#     return redirect(url_for('continue_view'), 301)

# @app.route('/counter/continue')
# def continue_view():
#     counter = request.cookies.get('counter') or 0
#     counter = int(counter) + 1
#     context = {}
#     context['counter'] = counter
#     response = make_response(
#         render_template('index.html',
#                         **context)
#     )
#     response.set_cookie('counter', str(counter).encode('utf-8'))
#     return response

# @app.route('/counter/reset')
# def reset_view():
#     counter = 0
#     context = {}
#     context['counter'] = counter
#     response = make_response(
#         render_template('index.html',
#                         **context)
#     )
#     response.set_cookie('counter', str(counter).encode('utf-8'))
#     return response
