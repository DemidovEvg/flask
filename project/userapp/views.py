from flask import Blueprint
from flask import render_template
from sqlalchemy import select
from project.models import User
from project.utils.plural_word import plural_word
from project.database import db

user_blueprint = Blueprint(
    name='userapp',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/users'
)


@user_blueprint.route('/', endpoint='user_list_view')
def user_list_view():
    users = db.session.query(User).all()
    return render_template('userapp/user_list.html', users=users)


@user_blueprint.route('/<int:id>', endpoint='user_detail_view')
def user_detail_view(id):
    user = db.session.query(User).filter(User.id == id).one()
    return render_template('userapp/user_detail.html', user=user, plural_word=plural_word)
