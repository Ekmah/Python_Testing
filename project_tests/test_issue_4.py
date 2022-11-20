from project_tests.conftest import *

# Assert1: points clubs after < points clubs before if reservation > 0.
# Assert2: Competition place taken == difference club points before/after


class TestIssue4:

    @staticmethod
    def assertions(before_points, after_points, before_places,
                   after_places, chosen_points):
        before_places = int(before_places)
        after_places = int(after_places)
        before_points = int(before_points)
        after_points = int(after_points)
        chosen_points = int(chosen_points)
        asserts = (
            ((before_places - after_places) == (before_points - after_points)),
            # if false, compets and clubs have not been deduced the same number
            ((before_places - after_places) == (before_points - after_points)
             and (before_places - after_places) <= 12),
            # if false, more than 12 places/points have been used
        )
        return asserts

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
        after_points = clubs[1]["points"]

        assert self.assertions(before_points, after_points, before_places,
                               after_places, chosen_points)

    def test_more_than_12(self, client):
        route = "/purchasePlaces"
        before_points = clubs[1]["points"]
        before_places = competitions[1]["numberOfPlaces"]
        chosen_points = 13
        response = client.post(route, data={
            "club": clubs[1]["name"],
            "competition": competitions[1]["name"],
            "places": chosen_points,
        })
        after_places = competitions[1]["numberOfPlaces"]
        after_points = clubs[1]["points"]

        assert self.assertions(before_points, after_points, before_places,
                               after_places, chosen_points)
