from flask import Blueprint, render_template, redirect
from flask_login import login_required
from werkzeug.exceptions import NotFound

article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../static')

ARTICLES = [
    {
        'id': 0,
        'title': 'some title #1',
        'text': 'some text',
        'author': {
            'name': 'some name0',
            'id': 1,
        },
    },
    {
        'id': 1,
        'title': 'some title #2',
        'text': 'some text',
        'author': {
            'name': 'some name1',
            'id': 2,
        },
    }
]


@article.route('/')
@login_required
def articles_list():
    return render_template('articles/list.html', articles=ARTICLES)


@article.route('/<int:pk>')
def get_article(pk):
    try:
        _article = ARTICLES[pk]
    except KeyError:
        # raise NotFound(f'User id {pk} not found')
        return redirect('/articles')
    return render_template('articles/detail.html', article=_article)
