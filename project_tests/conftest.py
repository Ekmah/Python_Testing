import pytest
from server import app, competitions, clubs, load_clubs, load_competitions


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client
