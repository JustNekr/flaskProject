from flask import Flask, request

from blog.user.views import user


# app = Flask(__name__)
#
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == 'GET':
#         return "This is a GET request", 200
#     elif request.method == "POST":
#         return "This is a POST request", 200

def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user)
