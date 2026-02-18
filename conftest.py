import pytest


@pytest.fixture
def base_url():
    return "https://api.restful-api.dev/objects"


@pytest.fixture
def context():
    return {}