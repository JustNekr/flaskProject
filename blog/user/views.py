from flask import Blueprint, render_template

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@user.route('/')
def users_list():
    return render_template('users/list.html')
