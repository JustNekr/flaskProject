from flask import Flask
from flask_login import LoginManager

from blog.article.views import article
from blog.auth.views import auth
from blog.commands import init_db, create_users
from blog.models.database import db
from blog.user.views import user


def register_commands(app: Flask):
    app.cli.add_command(init_db, 'init_db')
    app.cli.add_command(create_users, 'create_users')
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(auth)


def register_db(app: Flask):
    db.init_app(app)


def register_login_manager(app: Flask):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from blog.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app
