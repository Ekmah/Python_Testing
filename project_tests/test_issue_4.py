from project_tests.conftest import *


class TestIssue4:

    @staticmethod
    def assertions(before_places, after_places):
        before_places = int(before_places)
        after_places = int(after_places)
        assert (before_places - after_places) <= 12

    def test_correct_amount(self, client):
        route = "/purchasePlaces"
        before_points = clubs[1]["points"]
        before_places = competitions[1]["numberOfPlaces"]
        chosen_points = int(before_points) - 1
        if chosen_points < 0 or chosen_points > 12:
            chosen_points = 0
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_places = competitions[1]["numberOfPlaces"]
        self.assertions(before_places, after_places)

    def test_more_than_12(self, client):
        route = "/purchasePlaces"
        before_places = competitions[1]["numberOfPlaces"]
        chosen_points = 13
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_places = competitions[1]["numberOfPlaces"]
        self.assertions(before_places, after_places)
