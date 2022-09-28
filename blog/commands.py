import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from blog.models.database import db
from blog.models.user import User


@click.command()
@with_appcontext
def init_db():
    """
    Create database and tables
    :return:
    """
    db.create_all()


@click.command()
@with_appcontext
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """

    admin = User(name="admin", email='admin@mail.com', password=generate_password_hash('admin', method='sha256'))
    james = User(name="james", email='james@mail.com', password=generate_password_hash('james', method='sha256'))
    db.session.add(admin)
    db.session.add(james)
    db.session.commit()
    print("done! created users:", admin, james)


