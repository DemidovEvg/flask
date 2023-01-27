from flask_login import LoginManager
from sqlalchemy.orm import Session
from project.database import db
from project.models import User


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
            session: Session = db.session
            return session.query(User).filter_by(id=user_id).one_or_none()

        return app
    return inner
