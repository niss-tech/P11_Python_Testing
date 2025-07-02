import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

# Chargement des données depuis les fichiers JSON
def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']

def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


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



@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    clubs_data = get_clubs()
    competitions_data = get_competitions()

    competition = next((c for c in competitions_data if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs_data if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Club or competition not found.")
        return redirect(url_for('index'))
    
    # S’assurer que les places demandées sont bien un entier
    try:
        placesRequired = int(request.form['places'])
    except ValueError:
        flash("Invalid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions_data)
    
    placesRequired = int(request.form['places'])

    # Règle métier ajoutée: interdire la réservation de plus de places que disponibles
    availablePlaces = int(competition['numberOfPlaces'])
    if placesRequired > availablePlaces:
        flash("Cannot book more places than are available in the competition.")
        return render_template('welcome.html', club=club, competitions=competitions_data)

    # Nouvelle règle : maximum 12 places par réservation
    if placesRequired > 12:
        flash("Cannot book more than 12 places")
        return render_template('welcome.html', club=club, competitions=competitions_data)
    
    # Vérifie si le club a suffisamment de points pour réserver
    if placesRequired > int(club['points']):
        flash("Not enough points")
        return render_template('booking.html', club=club, competition=competition)


    # Mise à jour des données
    competition['numberOfPlaces'] = str(int(availablePlaces) - placesRequired)
    club['points'] = str(int(club['points']) - placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions_data)


@app.route('/points')
def display_points():
    clubs_data = get_clubs()  # Accès aux données dynamiques comme dans les autres routes
    return render_template('points.html', clubs=clubs_data)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))