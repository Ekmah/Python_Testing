from project_tests.conftest import *

# Assert1: points clubs after < points clubs before if reservation > 0.
# Assert2: Competition place taken == difference club points before/after


class TestIssue2:

    @staticmethod
    def assertions(before_points, after_points, chosen_points):
        before_points = int(before_points)
        after_points = int(after_points)
        chosen_points = int(chosen_points)
        asserts = (
            ((before_points - after_points) == chosen_points),
            # if false, places have not been deduced properly from clubs
            after_points >= 0,
            # if false, points are in the negatives
            (before_points == after_points
             and chosen_points == 0)
            # If no places are taken, no place/points should be deducted
        )
        return asserts

    def test_more_than_available_points(self, client):
        route = "/purchasePlaces"
        before_points = clubs[1]["points"]
        chosen_points = int(before_points) + 1
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_points = clubs[1]["points"]

        assert self.assertions(before_points, after_points, chosen_points)

    def test_correct_amount(self, client):
        route = "/purchasePlaces"
        before_points = clubs[1]["points"]
        chosen_points = int(before_points) - 1
        if chosen_points < 0:
            chosen_points = 0
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_points = clubs[1]["points"]

        assert self.assertions(before_points, after_points, chosen_points)

    def test_null_amount(self, client):
        route = "/purchasePlaces"
        before_points = clubs[1]["points"]
        chosen_points = 0
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_points = clubs[1]["points"]

        assert self.assertions(before_points, after_points, chosen_points)

    def test_negative_amount(self, client):
        route = "/purchasePlaces"
        before_points = clubs[1]["points"]
        chosen_points = -1
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_points = clubs[1]["points"]

        assert self.assertions(before_points, after_points, chosen_points)
