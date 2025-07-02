import json
from flask import Flask,render_template,request,redirect,flash,url_for


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
    # Récupère les données dynamiques selon le contexte (normal ou test)
    clubs_data = get_clubs()
    competitions_data = get_competitions()

    # Recherche du club et de la compétition envoyés dans le formulaire
    competition = next((c for c in competitions_data if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs_data if c['name'] == request.form['club']), None)

    placesRequired = int(request.form['places'])

     # Mise à jour du nombre de places et des points du club
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
    club['points'] = str(int(club['points']) - placesRequired) 


    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions_data)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))