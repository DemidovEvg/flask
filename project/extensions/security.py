from flask_bcrypt import Bcrypt

flask_bcrypt = Bcrypt()


def attach_flask_bcrypt(func):
    def inner(*args, **kwargs):
        app = func(*args, **kwargs)
        flask_bcrypt.init_app(app)
        return app
    return inner
