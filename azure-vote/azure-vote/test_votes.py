import os
import tempfile

import pytest
from flask_api import status

from main import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):

    with app.test_client() as client:
        # with app.app_context():
        #     init_db()
        yield client

# def test_db_call(app, client):
#     """Database select request should not fail"""

#     rv = client.get('/results')
#     assert status.is_success(rv.status_code)
#     # assert b'()' in rv.data


def test_health(app, client):
    """Health call should return successful status code"""
    rv = client.get('/health')
    assert status.is_success(rv.status_code)

def test_prod(app, client):
    """Return status 500 if env='prod'"""
    app.config['env'] = 'prod'
    rv = client.get('/')
    assert status.HTTP_500_INTERNAL_SERVER_ERROR == rv.status_code

@pytest.mark.skipif(os.getenv("TEST_LEVEL", '') != "all",reason="always fails")
def test_fail(app, client):
    """This test is always failing"""
    assert False