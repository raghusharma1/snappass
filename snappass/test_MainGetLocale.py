import pytest
from flask import Flask
from flask_babel import Babel
from main import get_locale

app = Flask(__name__)
babel = Babel(app)

@app.route('/')
def home():
    return get_locale()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.valid
def test_get_locale_priority_english(client):
    # Arrange: Mock flask request object with English (en) having the highest quality value in the accepted languages.
    client.environ_base['HTTP_ACCEPT_LANGUAGE'] = 'en;q=1,es;q=0.9'
    
    # Act: Call the get_locale function.
    response = client.get('/')
    
    # Assert: Check if the returned value matches 'en'.
    assert response.data == 'en'

@pytest.mark.valid
def test_get_locale_multiple_languages(client):
    # Arrange: Mock flask request object with multiple languages in accept_languages where Spanish ('es') has the highest quality value.
    client.environ_base['HTTP_ACCEPT_LANGUAGE'] = 'es;q=1,en;q=0.9,de;q=0.8'
    
    # Act: Call the get_locale function.
    response = client.get('/')
    
    # Assert: Check if the returned value matches 'es'.
    assert response.data == 'es'

@pytest.mark.invalid
def test_get_locale_unsupported_language(client):
    # Arrange: Mock the flask request object so the highest quality value corresponds to a language not supported by the function (let's say 'ru').
    client.environ_base['HTTP_ACCEPT_LANGUAGE'] = 'ru;q=1,es;q=0.9'
    
    # Act: Call the get_locale function.
    response = client.get('/')
    
    # Assert: Check if the returned value is None.
    assert response.data is None
