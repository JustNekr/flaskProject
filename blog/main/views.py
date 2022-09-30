from flask import Blueprint, render_template, redirect


main = Blueprint('main', __name__, url_prefix='', static_folder='../static')


@main.route('/')
def index():
    return render_template('base.html')

