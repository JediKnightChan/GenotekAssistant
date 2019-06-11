import pytest
from alice import alice, db


@pytest.fixture
def client():
    alice.app.config['TESTING'] = True
    client = alice.app.test_client()
    db.create_all()
    yield client

