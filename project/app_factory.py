import os
from dotenv import load_dotenv

from flask import Flask, redirect, url_for, jsonify
from flask_swagger import swagger
from flask_sqlalchemy import SQLAlchemy
from project.database import db, migrate
from project.extensions import attach_login_manager, attach_flask_bcrypt
from project.userapp.views import user_blueprint
from project.truckapp.views import truck_blueprint
from project.authapp.views import auth_blueprint
from project.apiapp import api
from project.commands import register_commands
from project.admin import admin

load_dotenv()


@attach_flask_bcrypt
@attach_login_manager
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_blueprints(app)
    register_db(app, db)
    register_commands(app)
    admin.init_app(app)
    api.init_api(app)

    # ==========================
    # Общие вьюхи
    @app.errorhandler(404)
    def page_not_found(error):
        return 'Не нашли что хотели'

    @app.route('/')
    def start_view():
        return redirect(url_for('userapp.user_list_view'), 301)

    @app.route("/spec")
    def spec():
        return jsonify(swagger(app))

    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(user_blueprint)
    app.register_blueprint(truck_blueprint)
    app.register_blueprint(auth_blueprint)


def register_db(app: Flask, db: SQLAlchemy) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
