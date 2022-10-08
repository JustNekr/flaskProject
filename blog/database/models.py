import datetime

from flask_login import UserMixin
from sqlalchemy import Table, func, select
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql.expression import exists

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


class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="appointments")

    barber_id = db.Column(db.Integer, db.ForeignKey('barber.id'))
    barber = relationship("Barber", back_populates="appointments")

    services = relationship("Service", secondary=appointment_service_association_table, back_populates="appointments")

    date = db.Column(db.Date)
    time = db.Column(db.Time)

    @hybrid_property
    def duration(self) -> datetime.timedelta:
        duration = datetime.timedelta()
        for service in self.services:
            duration += service
        return duration

    @hybrid_property
    def time_end(self) -> datetime.time:
        end_date = datetime.datetime.combine(self.date, self.time) + self.duration
        return end_date.time()


class Barber(db.Model):
    __tablename__ = "barber"
    id = db.Column(db.Integer, primary_key=True)
    work_place = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = relationship("User", back_populates="barber", uselist=False)
    services = relationship("Service", secondary=barber_service_association_table, back_populates="barbers")
    appointments = relationship("Appointment", back_populates="barber")
    day_schedules = relationship("DaySchedule", back_populates="barber")

    @hybrid_method
    def appointments_for_date(self, date: datetime.date) -> list[Appointment]:
        return [appointment for appointment in self.appointments if appointment.date == date]

    # @hybrid_method
    # def test(self, date):
    #     (select([func.count(Child.child_id)]).
    #      where(Child.parent_id == cls.parent_id).
    #      where(Child.time >= stime).
    #      where(Child.time <= etime).
    #      label("child_count")
    #      )


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(100))

    barber = relationship("Barber", back_populates="user", uselist=False)
    appointments = relationship("Appointment", back_populates="user")

    is_barber = column_property(
        exists().where(Barber.user_id == id)
    )
    is_staff = db.Column(db.Boolean(), default=False)


class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    duration = db.Column(db.Interval)
    description = db.Column(db.String(1000))
    barbers = relationship("Barber", secondary=barber_service_association_table, back_populates="services")
    appointments = relationship("Appointment", secondary=appointment_service_association_table, back_populates="services")


class DaySchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber.id'))
    barber = relationship("Barber", back_populates="day_schedules")

    @hybrid_property
    def interval_list(self) -> list[datetime.time]:
        interval_list = []
        start_date = datetime.datetime.combine(self.date, self.time_start)
        end_date = datetime.datetime.combine(self.date, self.time_end)
        delta = datetime.timedelta(minutes=30)
        while start_date < end_date:
            interval_list.append(start_date.time())
            start_date += delta
        return interval_list

    @hybrid_property
    def schedule(self) -> list:
        schedule: list = []
        interval_list: list[datetime.time] = self.interval_list
        appointments: list[Appointment] = self.barber.appointments_for_date(self.date)

        for interval in interval_list:
            is_free = True
            for appointment in appointments:
                if appointment.time > interval > appointment.time_end:
                    is_free = False
            schedule_item = (interval.strftime("%H:%M"), is_free)
            schedule.append(schedule_item)
        return schedule

