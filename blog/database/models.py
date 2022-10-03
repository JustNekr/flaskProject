from flask_login import UserMixin
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from blog.database import db


barber_service_association_table = Table(
    "barber_service_association",
    db.metadata,
    db.Column("barber_id", db.ForeignKey("barber.id"), primary_key=True),
    db.Column("service_id", db.ForeignKey("service.id"), primary_key=True),
)


appointment_service_association_table = Table(
    "appointment_service_association",
    db.metadata,
    db.Column("appointment_id", db.ForeignKey("appointment.id"), primary_key=True),
    db.Column("service_id", db.ForeignKey("service.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(100))

    barber = relationship("Barber", back_populates="user", uselist=False)
    appointments = relationship("Appointment", back_populates="user")


class Barber(db.Model):
    __tablename__ = "barber"
    id = db.Column(db.Integer, primary_key=True)
    work_place = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="barber", uselist=False)
    services = relationship("Service", secondary=barber_service_association_table, back_populates="barbers")


class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    duration = db.Column(db.Time)
    description = db.Column(db.String(1000))
    barbers = relationship("Barber", secondary=barber_service_association_table, back_populates="services")
    appointments = relationship("Appointment", secondary=appointment_service_association_table, back_populates="services")


class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="appointments")

    barber_id = db.Column(db.Integer, db.ForeignKey('barber.id'))
    barber = relationship("Barber", back_populates="appointments")

    services = relationship("Service", secondary=appointment_service_association_table, back_populates="appointments")

    date = db.Column(db.DateTime)


