from flask import Blueprint
from flask import render_template
from flask import current_app
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from project.models import User
from project.utils.plural_word import plural_word
from project.database import db

session: Session = db.session

user_blueprint = Blueprint(
    name='userapp',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/users'
)


@user_blueprint.route('/', endpoint='user_list_view')
def user_list_view():
    users = session.query(User).all()
    return render_template('userapp/user_list.html', users=users)


@user_blueprint.route('/<int:id>', endpoint='user_detail_view')
def user_detail_view(id):
    try:
        user = session.query(User).filter(User.id == id).one()
    except NoResultFound as exc:
        current_app.logger.error(exc)
        raise

    return render_template('userapp/user_detail.html', user=user, plural_word=plural_word)
