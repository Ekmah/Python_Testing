import pytest
import json
import os
from flask import Flask
from server import app, competitions, clubs


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client

