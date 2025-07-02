from locust import HttpUser, task, between

class GUDLFTUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # Simulation d'une "connexion" avec un email valide
        self.club_email = "john@simplylift.co"
        self.club_name = "Simply Lift"
        self.competition_name = "Spring Festival"

        self.client.post("/showSummary", data={"email": self.club_email})

    @task
    def view_booking_page(self):
        # Accès à la page de réservation pour une compétition
        self.client.get(f"/book/{self.competition_name}/{self.club_name}")

    @task
    def purchase_places(self):
        # Envoi d'une réservation de places (valide)
        self.client.post("/purchasePlaces", data={
            "club": self.club_name,
            "competition": self.competition_name,
            "places": "1"
        }, allow_redirects=True)
