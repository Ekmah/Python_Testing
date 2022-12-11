import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './clubs.json')
    with open(filename) as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './competitions.json')
    with open(filename) as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    try:
        club = \
            [club for club in clubs if club['email'] == request.form['email']][
                0]
    except IndexError:
        return "Sorry, that email wasn't found."
    return render_template('welcome.html', club=club, clubs=clubs,
                           competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = \
        [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        possible_places = min(int(found_club['points']),
                              min(12,
                                  int(found_competition['numberOfPlaces'])))
        comp_time = datetime.strptime(found_competition["date"],
                                      "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        available = comp_time >= now
        found_competition["available"] = available
        if not available:
            return "Sorry, that competition has passed."
        else:
            return render_template('booking.html', club=found_club, 
                                   competition=found_competition,
                                   possible_places=possible_places)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, clubs=clubs,
                               competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = \
        [c for c in competitions if c['name'] ==
         request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    if (
            places_required > 12 or
            (places_required > int(club["points"])) or
            (places_required > int(competition['numberOfPlaces'])) or
            places_required <= 0):
        return "You are trying to book an impossible quantity of places."
    competition['numberOfPlaces'] = \
        int(competition['numberOfPlaces']) - places_required
    club["points"] = int(club["points"]) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, clubs=clubs,
                           competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
