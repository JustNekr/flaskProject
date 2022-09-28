from flask import Blueprint, render_template, redirect
from werkzeug.exceptions import NotFound

from blog.models.user import User

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@user.route('/')
def users_list():
    _users = User.query.all()
    return render_template('users/list.html', users=_users)


@user.route('/<int:pk>')
def get_user(pk):
    try:
        _user = User.query.filter_by(id=pk).first()
    except Exception:
        # raise NotFound(f'User id {pk} not found')
        return redirect('/users')
    return render_template('users/detail.html', user=_user)
