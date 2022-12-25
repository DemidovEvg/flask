from flask import Blueprint, g
from flask import render_template
from sqlalchemy import select
from models import User
from project.utils.plural_word import plural_word

user_blueprint = Blueprint(
    name='user',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/users'
)


@user_blueprint.route('/', endpoint='user_list_view')
def user_list_view():
    query = select(User)
    users = g.session.execute(query).all()
    users = [user[0] for user in users]
    return render_template('user/user_list.html', users=users)


@user_blueprint.route('/<int:id>', endpoint='user_detail_view')
def user_detail_view(id):
    user = g.session.query(User).filter(User.id == id).one()
    return render_template('user/user_detail.html', user=user, plural_word=plural_word)
