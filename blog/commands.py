import datetime

import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from blog.database import db
from blog.database.models import User, Barber, Service


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

    admin = User(name="admin", email='admin@mail.com', password=generate_password_hash('admin', method='sha256'),
                 is_staff=True)
    db.session.add(admin)
    for num in range(10):
        user = User(name=f"user_{num}", email=f'user_{num}@mail.com', password=generate_password_hash(f'user_{num}', method='sha256'))
        db.session.add(user)
        db.session.flush()
        if num % 2 == 0:
            barber = Barber(work_place=f'user_{num}_workplace', user_id=user.id)
            db.session.add(barber)

    db.session.commit()

    print("done! created users:", admin)


@click.command()
@with_appcontext
def create_services():
    """
    Create services in database
    :return:
    """

    basic_services = [
        ('Мужская стрижка', 1500, datetime.timedelta(minutes=60), 'стрижка замороченная'),
        ('Моделирование бороды', 1100, datetime.timedelta(minutes=45), 'норм'),
        ('Детская стрижка', 1100, datetime.timedelta(minutes=45), 'че так дорого он же мелкий'),
        ('Стрижка отца и сына', 2100, datetime.timedelta(minutes=60), 'оптом дешевле'),
        ('Мужская стрижка + моделирование бороды', 2200, datetime.timedelta(minutes=90), 'выйдешь красавцем'),
        ('Королевское бритьё', 1500, datetime.timedelta(minutes=45), 'херь какая-то'),
        ('Эпиляция воском: 1 зона', 400, datetime.timedelta(minutes=15), 'уши, ноздри и всякое такое'),
        ('Камуфляж седых волос', 100, datetime.timedelta(minutes=30), 'бежишь от старости?'),
        ('Стрижка машинкой', 800, datetime.timedelta(minutes=30), 'дешево и сердито'),
        ('Бритьё головы', 1200, datetime.timedelta(minutes=45), 'почему-то дольше чем стрижка машинкой'),

    ]
    for service in basic_services:
        name, price, duration, description = service
        new_service = Service(name=name, price=price, duration=duration, description=description)
        db.session.add(new_service)
    db.session.commit()


@click.command()
@with_appcontext
def associate_services():
    barbers = Barber.query.all()
    services = Service.query.all()
    for barber in barbers:
        if barber.id % 2 == 0:
            barber_services = [service for service in services if service.id % 2 == 0]
            for service in barber_services:
                barber.services.append(service)
                db.session.add(barber)
        else:
            barber_services = [service for service in services if service.id % 2 != 0]
            for service in barber_services:
                barber.services.append(service)
                db.session.add(barber)
    db.session.commit()
