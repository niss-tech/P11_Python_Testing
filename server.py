import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)



@app.route('/book/<competition>/<club>')
def book(competition, club):
    # Récupération des données dynamiques, selon que l’on soit en mode test ou exécution normale
    clubs_data = get_clubs()
    competitions_data = get_competitions()

    # Recherche du club et de la compétition dans les données
    foundClub = next((c for c in clubs_data if c['name'] == club), None)
    foundCompetition = next((c for c in competitions_data if c['name'] == competition), None)

    # Si club ou compétition introuvables → redirection avec message
    if not foundClub or not foundCompetition:
        flash("Club or competition not found.")
        return redirect(url_for('index'))

    # Vérifie que la date de la compétition est dans le futur
    competition_date = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("You cannot book a competition that has already taken place.")
        return render_template('welcome.html', club=foundClub, competitions=competitions_data)

    # Si tout est bon, afficher la page de réservation
    return render_template('booking.html', club=foundClub, competition=foundCompetition)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))