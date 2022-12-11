from project_tests.conftest import *

# Assert1: points clubs after < points clubs before if reservation > 0.
# Assert2: Competition place taken == difference club points before/after


class TestIssue2:

    def test_more_than_available_points(self, client):
        route = "/purchasePlaces"
        before_points = int(clubs[1]["points"])
        before_places = int(competitions[1]["numberOfPlaces"])
        chosen_points = int(before_points) + 1
        response = client.post(route, data={
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

    def test_more_than_available_places(self, client):
        route = "/purchasePlaces"
        before_points = clubs[1]["points"]
        before_places = competitions[1]["numberOfPlaces"]
        chosen_points = int(before_places) + 1
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_places = competitions[1]["numberOfPlaces"]
        after_points = clubs[1]["points"]

        assert ((before_places - after_places) <= before_points or
                (before_places - after_places) <= 12)
        assert (before_places - after_places) == chosen_points
        assert (before_points - after_points) == chosen_points
        assert (before_places - after_places) == (before_points - after_points)
        assert after_places >= 0
        assert after_points >= 0

    def test_correct_amount(self, client):
        route = "/purchasePlaces"
        before_points = clubs[1]["points"]
        before_places = competitions[1]["numberOfPlaces"]
        chosen_points = int(before_points) - 1
        if chosen_points < 0:
            chosen_points = 0
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_places = competitions[1]["numberOfPlaces"]
        after_points = clubs[1]["points"]

        assert ((before_places - after_places) <= before_points or
                (before_places - after_places) <= 12)
        assert (before_places - after_places) == chosen_points
        assert (before_points - after_points) == chosen_points
        assert (before_places - after_places) == (before_points - after_points)
        assert after_places >= 0
        assert after_points >= 0
