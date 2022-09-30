from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from blog.models.database import db
from blog.models.user import User

auth = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.users_list'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'warning')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    flash('Login success', 'success')
    return redirect(request.args.get('next') or url_for('user.users_list'))


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    print(email)
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists', 'warning')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    flash('Signup success', 'success')
    return redirect(url_for('auth.login'))
