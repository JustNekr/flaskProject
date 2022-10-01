from flask import Flask
from blog.extensions import register_blueprints, register_commands, register_db, register_login_manager, \
    register_migrate, register_csrf


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object('blog.config')

    register_blueprints(app)
    register_commands(app)
    register_db(app)
    register_migrate(app)
    register_login_manager(app)
    register_csrf(app)

    return app

