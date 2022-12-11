import json
import os
from datetime import datetime
from flask import session
from project_tests.conftest import *
from server import book


class TestIssue1:
    def test_not_email(self, client):
        email = "aaaaaaaaaa"
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assertion = \
            b"Sorry, that email wasn't found."
        assert response.data == assertion

    def test_wrong_email(self, client):
        email = "test.test@test.fr"
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assertion = \
            b"Sorry, that email wasn't found."
        assert response.data == assertion

    def test_good_email(self, client):
        email = clubs[0]['email']
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assert response.status_code == 200

    def test_other_type(self, client):
        email = 1
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assertion = \
            b"Sorry, that email wasn't found."
        assert response.data == assertion


class TestIssue2:

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
        assert resp.data == assertion


class TestIssue5:

    def test_future_competition_date(self, client):
        competition = competitions[2]["name"]
        club = clubs[1]["name"]

        resp = client.get(f"/book/{competition}/{club}")
        assert resp.data != b'Sorry, that competition has passed.'

    def test_past_competition_date(self, client):
        competition = competitions[1]["name"]
        club = clubs[1]["name"]

        resp = client.get(f"/book/{competition}/{club}")
        assert resp.data == b'Sorry, that competition has passed.'


