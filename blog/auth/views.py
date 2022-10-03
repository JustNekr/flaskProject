from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from blog.forms.auth import LoginForm, RegisterForm
from blog.database import db
from blog.database.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one_or_none()
        if user and check_password_hash(user.password, form.password.data):
            rm = form.remember.data
            login_user(user, remember=rm)
            flash('Login success', 'success')
            return redirect(request.args.get("next") or url_for("main.index"))

        flash("Неверная пара логин/пароль", "danger")

    return render_template("auth/login.html", title="Авторизация", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.users_list'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password_hash = generate_password_hash(form.password.data, method='sha256')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'warning')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, name=name, password=password_hash)

        db.session.add(new_user)
        db.session.commit()
        flash('Signup success', 'success')
        return redirect(url_for('auth.login'))

    return render_template("auth/signup.html", title="Регистрация", form=form)
