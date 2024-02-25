import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    response = client.get('/data')
    assert response.status_code == 200


def test_insert_data(client):
    # Datos de prueba a insertar
    test_data = {"name": "Test Name"}
    response = client.post('/data', json=test_data)
    assert response.status_code == 200
    assert response.json['message'] == "Data inserted successfully"
