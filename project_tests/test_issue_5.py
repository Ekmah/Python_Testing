import json
import os
from datetime import datetime
from flask import session
from project_tests.conftest import *
from server import book


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
