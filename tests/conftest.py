from api_organiza_ai import create_app, Flask
from api_organiza_ai.extensions import db
import pytest

@pytest.fixture(scope='session')
def app():
    app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///storage_test.db',
    })

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()

@pytest.fixture()
def client(app: Flask):
    return app.test_client()