import json
from flask import Flask, render_template, request, redirect, flash, url_for

# Chargement des données depuis les fichiers JSON
def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']

def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']

# Application Flask
app = Flask(__name__)
app.secret_key = 'something_special'

# Données globales par défaut
clubs = loadClubs()
competitions = loadCompetitions()

# Accès aux données en fonction du contexte (tests ou run normal)
def get_clubs():
    return getattr(app, 'clubs', clubs)

def get_competitions():
    return getattr(app, 'competitions', competitions)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    clubs_data = get_clubs()
    competitions_data = get_competitions()

    competition = next((c for c in competitions_data if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs_data if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Club or competition not found.")
        return redirect(url_for('index'))

    try:
        placesRequired = int(request.form['places'])
    except ValueError:
        flash("Invalid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions_data)

    availablePlaces = int(competition['numberOfPlaces'])

    if placesRequired > availablePlaces:
        flash("Cannot book more places than are available in the competition.")
        return render_template('welcome.html', club=club, competitions=competitions_data)


    competition['numberOfPlaces'] = str(availablePlaces - placesRequired)
    club['points'] = str(int(club['points']) - placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions_data)

# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
