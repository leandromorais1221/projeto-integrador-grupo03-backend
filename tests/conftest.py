from api_organiza_ai import create_app, Flask
from api_organiza_ai.extensions import db
import pytest
from actions.auth_action import AuthAction


@pytest.fixture(scope='session')
def app():
    app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///storage_test.db',
        'JWT_SECRET_KEY': '0b2a47e4bd4e614dd05a5eca3f5c26b08c39cc7c0e5faa86ddf7141d5568a625'
    })

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()

@pytest.fixture()
def client(app: Flask):
    return app.test_client()

@pytest.fixture()
def auth(client):
    return AuthAction(client)



