from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from blog.admin import admin
from blog.article.views import article
from blog.auth.views import auth
from blog.commands import init_db, create_users, create_services, associate_services
from blog.main.views import main
from blog.database import db
from blog.database.models import User
from blog.user.views import user


def register_commands(app: Flask):
    app.cli.add_command(init_db, 'init_db')
    app.cli.add_command(create_users, 'create_users')
    app.cli.add_command(create_services, 'create_services')
    app.cli.add_command(associate_services, 'associate_services')


def register_blueprints(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(auth)
    app.register_blueprint(main)


def register_db(app: Flask):
    db.init_app(app)


def register_migrate(app: Flask):
    migrate = Migrate()
    migrate.init_app(app, db, compare_type=True)


def register_login_manager(app: Flask):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Authorize plz'
    login_manager.login_message_category = 'success'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_csrf(app: Flask):
    csrf = CSRFProtect()
    csrf.init_app(app)


def register_admin(app: Flask):
    admin.init_app(app)
