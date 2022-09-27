from werkzeug.security import generate_password_hash

from blog.app import create_app
from blog.models.database import db
from blog.models.user import User

app = create_app()


@app.cli.command('init-db')
def init_db():
    db.create_all()


@app.cli.command("create-users")
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


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
    )
