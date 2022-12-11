from project_tests.conftest import *

# Assert1: points clubs after < points clubs before if reservation > 0.
# Assert2: Competition place taken == difference club points before/after


class TestIssue2:

    def test_correct_update(self, client):
        route = "/purchasePlaces"
        before_points = int(clubs[1]["points"])
        if before_points == 0:
            chosen_points = 0
        else:
            chosen_points = 1
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_points = int(clubs[1]["points"])

        assert (before_points - after_points) == chosen_points
