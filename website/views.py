"""Routes for the website."""

from os import environ

from dotenv import load_dotenv
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user

from .scraping import scrape_kojo, get_website_name, scrape_seasons, get_kojo_sizes
from .database import insert_plant_data, insert_subscription, get_db_conn, is_plant_in_db, get_user_plants, is_user_subbed, insert_price, remove_sub

PFAS_WEBSITE = 'plantsforallseasons'
KOJO_WEBSITE = 'houseofkojo'

views = Blueprint('views', __name__)

load_dotenv()


@views.route("/")
@login_required
def home():
    db_conn = get_db_conn(environ)
    user_plants = get_user_plants(db_conn, current_user.get_id())
    return render_template('home.html', user=current_user, plants=user_plants)


@views.route("/add_plant", methods=["GET", "POST"])
@login_required
def add_plant():

    if request.method == "GET":
        return render_template('add_plant.html', user=current_user)

    db_conn = get_db_conn(environ)

    plant_url = request.form.get('plant_url')
    website_name = get_website_name(plant_url)
    if website_name not in [PFAS_WEBSITE, KOJO_WEBSITE]:
        flash('Website not compatible')
        return render_template('add_plant.html', user=current_user)
    if website_name == PFAS_WEBSITE:
        plant_data = scrape_seasons(plant_url)
        if not is_plant_in_db(db_conn, plant_data):
            insert_plant_data(db_conn, plant_data)
        if not is_user_subbed(db_conn, current_user.get_id(), plant_data):
            insert_subscription(db_conn, plant_data, current_user.get_id())
            insert_price(db_conn, plant_data)
        return render_template('plant_submitted.html', user=current_user, plant=plant_data)
    session['plant_url'] = plant_url
    return redirect(url_for('views.choose_size'))


@views.route("/choose_size", methods=["GET", "POST"])
@login_required
def choose_size():
    plant_url = session['plant_url']
    if request.method == "GET":
        sizes = get_kojo_sizes(plant_url)
        return render_template('choose_size.html', user=current_user, sizes=sizes)
    db_conn = get_db_conn(environ)
    size = request.form.get('size')
    plant_data = scrape_kojo(plant_url, size)
    if not is_plant_in_db(db_conn, plant_data):
        insert_plant_data(db_conn, plant_data)
    if not is_user_subbed(db_conn, current_user.get_id(), plant_data):
        insert_subscription(db_conn, plant_data, current_user.get_id())
        insert_price(db_conn, plant_data)
    return render_template('plant_submitted.html', user=current_user, plant=plant_data)


@views.route("/delete_plant/<int:plant_id>", methods=["POST"])
@login_required
def delete_plant(plant_id: int):
    """Endpoint which removes the plant from the users subscription."""

    db_conn = get_db_conn(environ)
    user_id = current_user.get_id()

    remove_sub(db_conn, user_id, plant_id)

    flash('Plant removed')

    return redirect(url_for('views.home'))
