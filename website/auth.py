"""Authentication routes for the website."""

from flask import Blueprint, request, render_template, flash, redirect, url_for

from .forms import RegistrationForm

auth = Blueprint('auth', __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    reg_form = RegistrationForm()
    if request.method == "POST" and reg_form.validate():
        username = reg_form.username.data
        password = reg_form.password.data
        print(f"{username} - {password}")
        flash('Success!')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=reg_form)


@auth.route("/login")
def login():
    return render_template('login.html')


@auth.route("logout")
def logout():
    return "<h1>Logout</h1>"
