from project_tests.conftest import *


class TestIssue1:
    def test_not_email(self, client):
        email = "aaaaaaaaaa"
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assert response.status_code == 200

    def test_wrong_email(self, client):
        email = "test.test@test.fr"
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assert response.status_code == 200

    def test_good_email(self, client):
        email = clubs[0]['email']
        route = "/showSummary"
        response = client.post(route, data={
            "email": email,
        })
        assert response.status_code == 200
