import json
import os
from datetime import datetime
from flask import session
from project_tests.conftest import *
from server import book


class TestIssue5:

    def test_future_competition_date(self, client):
        route = "/showSummary"
        response = client.post(route, data={
            "email": clubs[1]["email"],
        })
        assert """<div id="clubs">""" in str(response.data)
        for club in clubs:  # check if all clubs are displayed.
            assert club["name"] in str(response.data)
