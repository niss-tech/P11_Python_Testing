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

competitions = loadCompetitions()
clubs = loadClubs()

# Accès aux données en fonction du contexte (tests ou run normal)
def get_clubs():
    return getattr(app, 'clubs', clubs)

def get_competitions():
    return getattr(app, 'competitions', competitions)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    # Récupère les données dynamiques actuelles des clubs et compétitions
    clubs_data = get_clubs()
    competitions_data = get_competitions()

    # Récupère l’email saisi dans le formulaire de connexion
    email_entered = request.form['email']

    # Cherche un club correspondant à cet email dans les données chargées
    matching_clubs = [club for club in clubs_data if club['email'] == email_entered]

    # Si aucun club ne correspond à l’email, on affiche un message d'erreur et on redirige vers l'accueil
    if not matching_clubs:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))

    # Si un club a été trouvé, on l’affiche avec la liste des compétitions dans la page d’accueil utilisateur
    club = matching_clubs[0]
    return render_template('welcome.html', club=club, competitions=competitions_data)



@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


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