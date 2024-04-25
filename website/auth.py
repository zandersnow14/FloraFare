"""Authentication routes for the website."""

from os import environ

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
import bcrypt
from dotenv import load_dotenv

from .database import get_db_conn, is_username_taken, is_email_taken, get_hashpw
from .forms import RegistrationForm, LoginForm
from .models import User

auth = Blueprint('auth', __name__)

load_dotenv()


@auth.route("/register", methods=["GET", "POST"])
def register():
    reg_form = RegistrationForm()
    if request.method == "POST" and reg_form.validate():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data
        hashpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        hashpw_dec = hashpw.decode()

        db_conn = get_db_conn(environ)

        if is_username_taken(db_conn, username):
            flash("Username already taken!", category="error")
            return render_template('register.html', form=reg_form, user=current_user)

        if is_email_taken(db_conn, email):
            flash("Email already taken!", category="error")
            return render_template('register.html', form=reg_form, user=current_user)

        with db_conn.cursor() as cur:
            cur.execute(
                query="""INSERT INTO users(username, email, password) VALUES (%s, %s, %s)""",
                vars=(username, email, hashpw_dec))
            db_conn.commit()

        print(f"{username} - {email} - {hashpw}")
        flash('Account successfully created!')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=reg_form, user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST" and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data

        db_conn = get_db_conn(environ)

        if not is_email_taken(db_conn, email):
            flash('Email does not exist')
            return render_template('login.html', form=login_form, user=current_user)

        hashpw = get_hashpw(db_conn, email)

        if bcrypt.checkpw(password.encode(), hashpw.encode()):
            flash('Logged in successfully!')
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

        else:
            flash('Incorrect password')

    return render_template('login.html', form=login_form, user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
