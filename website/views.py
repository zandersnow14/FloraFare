"""Routes for the website."""

from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user

from .scraping import scrape_kojo, get_website_name, scrape_seasons, get_kojo_sizes

PFAS_WEBSITE = 'plantsforallseasons'
KOJO_WEBSITE = 'houseofkojo'

views = Blueprint('views', __name__)


@views.route("/")
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route("/add_plant", methods=["GET", "POST"])
@login_required
def add_plant():

    if request.method == "GET":
        return render_template('add_plant.html', user=current_user)

    plant_url = request.form.get('plant_url')
    website_name = get_website_name(plant_url)
    if website_name not in [PFAS_WEBSITE, KOJO_WEBSITE]:
        flash('Website not compatible')
        return render_template('add_plant.html', user=current_user)
    if website_name == PFAS_WEBSITE:
        plant_data = scrape_seasons(plant_url)
        print(plant_data)
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
    size = request.form.get('size')
    plant_data = scrape_kojo(plant_url, size)
    return render_template('plant_submitted.html', user=current_user, plant=plant_data)
