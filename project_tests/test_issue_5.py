import json
import os
from datetime import datetime
from flask import session
from project_tests.conftest import *
from server import book


class TestIssue5:

    def test_future_competition_date(self, client):
        route = "/purchasePlaces"
        before_points = int(clubs[1]["points"])
        before_places = int(competitions[2]["numberOfPlaces"])
        comp_time = datetime.strptime(competitions[2]["date"],
                                      "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        available = comp_time >= now
        chosen_points = 1
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[2]["name"],
            "places": chosen_points,
        })
        after_places = int(competitions[2]["numberOfPlaces"])
        after_points = int(clubs[1]["points"])
        assert available
        # assert (before_places - after_places) == (before_points - after_points)
        assert (before_places - after_places) != 0

    def test_past_competition_date(self, client):
        route = "/purchasePlaces"
        before_points = int(clubs[1]["points"])
        before_places = int(competitions[1]["numberOfPlaces"])
        comp_time = datetime.strptime(competitions[1]["date"],
                                      "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        available = comp_time >= now
        chosen_points = 1
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_places = int(competitions[1]["numberOfPlaces"])
        after_points = int(clubs[1]["points"])
        assert available
        # assert (before_places - after_places) == (before_points - after_points)
        assert (before_places - after_places) != 0

    def test_test(self):
        pass
        # TODO statut des variables de book, (états) [IMPOSSIBLE]

    def test_access_session(self, client):
        competition = competitions[1]["name"]
        club = clubs[1]["name"]

        resp = client.get(f"/book/{competition}/{club}")
        assert resp.data == 0
