from project_tests.conftest import *


def test_integration(client):
    clubs_l = load_clubs()
    competitions_l = load_competitions()

    client.get("/")

    competition = competitions_l[2]
    club = clubs_l[1]

    email = club['email']
    client.post("/showSummary", data={"email": email})

    client.get(f"/book/{competition['name']}/{club['name']}")

    before_points = int(club["points"])
    # choose valid amount of points:
    if before_points == 0:
        chosen_points = 0
    else:
        chosen_points = 1
    client.post("/purchasePlaces", data={
        "club": club["name"],
        "competition": competition["name"],
        "places": chosen_points,
    })

    client.get('/logout')


def test_load_clubs():
    results = load_clubs()
    assert isinstance(results, list)
    assert isinstance(results[0], dict)


def test_load_competitions():
    results = load_competitions()
    assert isinstance(results, list)
    assert isinstance(results[0], dict)


def test_index(client):
    route = "/"
    response = client.get(route)
    assert response.status_code == 200


class TestShowSummary:

    def test_not_email(self, client):
        email = "aaaaaaaaaa"
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assertion = \
            b"Sorry, that email wasn't found."
        assert response.status_code == 200
        assert response.data == assertion

    def test_wrong_email(self, client):
        email = "test.test@test.fr"
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assertion = \
            b"Sorry, that email wasn't found."
        assert response.status_code == 200
        assert response.data == assertion

    def test_good_email(self, client):
        email = clubs[0]['email']
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assertion = \
            b"Sorry, that email wasn't found."
        assert response.status_code == 200
        assert response.data != assertion

    def test_other_type(self, client):
        email = 1
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assertion = \
            b"Sorry, that email wasn't found."
        assert response.status_code == 200
        assert response.data == assertion


class TestBook:

    def test_future_competition_date(self, client):
        competition = competitions[2]["name"]
        club = clubs[1]["name"]

        resp = client.get(f"/book/{competition}/{club}")
        assert resp.status_code == 200
        assert resp.data != b'Sorry, that competition has passed.'

    def test_past_competition_date(self, client):
        competition = competitions[1]["name"]
        club = clubs[1]["name"]

        resp = client.get(f"/book/{competition}/{club}")
        assert resp.status_code == 200
        assert resp.data == b'Sorry, that competition has passed.'

    def test_possible_places_points(self, client):
        competition = competitions[2]["name"]  # places are 13
        club = clubs[1]["name"]  # points are 4

        resp = client.get(f"/book/{competition}/{club}")
        assert resp.status_code == 200
        assert resp.data != b'Sorry, that competition has passed.'
        assert b"max='4'" in resp.data

    def test_possible_places_12(self, client):
        competition = competitions[2]["name"]  # places are 13
        club = clubs[0]["name"]  # points is 13

        resp = client.get(f"/book/{competition}/{club}")
        assert resp.status_code == 200
        assert resp.data != b'Sorry, that competition has passed.'
        assert b"max='12'" in resp.data

    def test_possible_places_places(self, client):
        competition = competitions[4]["name"]  # places are 3
        club = clubs[0]["name"]  # points is 13

        resp = client.get(f"/book/{competition}/{club}")
        assert resp.status_code == 200
        assert resp.data != b'Sorry, that competition has passed.'
        assert b"max='3'" in resp.data


class TestPurchasePlaces:

    def test_more_than_available_points(self, client):
        route = "/purchasePlaces"
        before_points = int(clubs[1]["points"])
        chosen_points = int(before_points) + 1
        resp = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        assertion = \
            b'You are trying to book an impossible quantity of places.'
        assert resp.status_code == 200
        assert resp.data == assertion

    def test_more_than_available_places(self, client):
        route = "/purchasePlaces"
        before_places = int(competitions[1]["numberOfPlaces"])
        chosen_points = int(before_places) + 1
        resp = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        assertion = \
            b'You are trying to book an impossible quantity of places.'
        assert resp.status_code == 200
        assert resp.data == assertion

    def test_more_than_12(self, client):
        route = "/purchasePlaces"
        chosen_points = 13
        resp = client.post(route, data={
            "club": clubs[0]["name"],
            "competition": competitions[3]["name"],
            "places": chosen_points,
        })
        assertion = \
            b'You are trying to book an impossible quantity of places.'
        assert resp.status_code == 200
        assert resp.data == assertion

    def test_correct_amount(self, client):
        route = "/purchasePlaces"
        before_points = int(clubs[1]["points"])
        before_places = int(competitions[1]["numberOfPlaces"])
        if before_points == 0:
            chosen_points = 0
        else:
            chosen_points = 1
        resp = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_places = int(competitions[1]["numberOfPlaces"])
        after_points = int(clubs[1]["points"])

        assert resp.status_code == 200
        assert ((before_places - after_places) <= before_points or
                (before_places - after_places) <= 12)
        assert (before_places - after_places) == chosen_points
        assert (before_points - after_points) == chosen_points
        assert (before_places - after_places) == (before_points - after_points)
        assert after_places >= 0
        assert after_points >= 0

    def test_null_amount(self, client):
        route = "/purchasePlaces"
        chosen_points = 0
        resp = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        assertion = \
            b'You are trying to book an impossible quantity of places.'
        assert resp.status_code == 200
        assert resp.data == assertion

    def test_negative_amount(self, client):
        route = "/purchasePlaces"
        chosen_points = -1
        resp = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        assertion = \
            b'You are trying to book an impossible quantity of places.'
        assert resp.status_code == 200
        assert resp.data == assertion
