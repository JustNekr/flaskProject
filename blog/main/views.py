from flask import Blueprint, render_template, redirect, request, jsonify, flash

from blog.database.models import Service, Barber
from blog.forms.auth import AppointmentForm

main = Blueprint('main', __name__, url_prefix='', static_folder='../static')


@main.route('/')
def index():
    return render_template('base.html')


@main.route('/services')
def services():
    _services = Service.query.all()
    return render_template('services.html', services=_services)


@main.route('/barbers')
def barbers():
    _barbers = Barber.query.all()
    return render_template('barbers.html', barbers=_barbers)


@main.route('/barbers_services/<int:pk>')
def barbers_services(pk):
    barber = Barber.query.filter_by(id=pk).first()
    _services = barber.services
    services_list = []
    for service in _services:
        service_object = {
            'id': service.id,
            'name': service.name
        }
        services_list.append(service_object)
    return jsonify({'services': services_list})
    # return render_template('services.html', services=_services)


@main.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm(request.form)
    barbers_list = Barber.query.all()
    form.barber.choices = [(barber.id, barber.user.name) for barber in barbers_list]

    barber_id = request.args.get('barber_id')
    if barber_id:
        form.barber.data = barber_id
        requested_barber = [barber for barber in barbers_list if barber.id == int(barber_id)][0]
        form.services.choices = [(service.id, service.name) for service in requested_barber.services]
    else:
        flash("Choose Barber First")

    return render_template("appointment.html", title="appointment", form=form)


