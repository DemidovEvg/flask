import os

from flask import (
    Flask,
    Response,
    request,
    make_response,
    render_template,
    redirect,
    url_for,
    g
)
from database import Database
from models import User


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    print(f'{app.instance_path=}')
    print(f'{app.config=}')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def stick_session():
        db = Database()
        session = db.db_session
        g.session = session
        g.current_user = session.query(User).filter_by(name="qwe").first()

    @app.route('/')
    @app.route('/counter/start', methods=['GET', 'POST'])
    def start_view():
        return redirect(url_for('continue_view'), 301)

    @app.route('/counter/continue')
    def continue_view():
        counter = request.cookies.get('counter') or 0
        counter = int(counter) + 1
        context = {}
        context['counter'] = counter
        response = make_response(
            render_template('index.html',
                            **context)
        )
        response.set_cookie('counter', str(counter).encode('utf-8'))
        return response

    @app.route('/counter/reset')
    def reset_view():
        counter = 0
        context = {}
        context['counter'] = counter
        response = make_response(
            render_template('index.html',
                            **context)
        )
        response.set_cookie('counter', str(counter).encode('utf-8'))
        return response

    @app.errorhandler(404)
    def page_not_found(error):
        return 'Не нашли что хотели'
    return app
