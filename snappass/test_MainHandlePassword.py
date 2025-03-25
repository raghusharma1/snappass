# Imports
import pytest
import os
import sys
import uuid
import redis
from unittest.mock import patch
from cryptography.fernet import Fernet
from flask import abort, Flask, render_template, request, jsonify, make_response
from redis.exceptions import ConnectionError
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from urllib.parse import urljoin
from distutils.util import strtobool
from flask_babel import Babel, _
from fakeredis import FakeStrictRedis

# Import the function to be tested
from main import handle_password

# Test Class
class Test_MainHandlePassword:

    @pytest.fixture
    def client(self):
        app = Flask(__name__)
        with app.test_client() as client:
            yield client

    @pytest.mark.valid
    def test_handle_password_valid_input(self, client):
        data = {'password': 'secure_password123', 'ttl': 'hour'}
        response = client.post('/handle_password', data=data)
        assert response.status_code == 200
        assert 'link' in response.data

    @pytest.mark.invalid
    @patch('main.clean_input', return_value=False)
    def test_handle_password_dirty_input(self, mock_clean_input, client):
        data = {'password': '><', 'ttl': 'hour'}
        response = client.post('/handle_password', data=data)
        assert response.status_code == 500

    @pytest.mark.valid
    def test_handle_password_json_mime(self, client):
        data = {'password': 'secure_password123', 'ttl': 'hour'}
        client.environ_base['HTTP_ACCEPT'] = 'application/json'
        response = client.post('/handle_password', data=data)
        assert response.status_code == 200
        assert 'link' in response.get_json()
        assert 'ttl' in response.get_json()

    @pytest.mark.valid
    def test_handle_password_html_mime(self, client):
        data = {'password': 'secure_password123', 'ttl': 'hour'}
        client.environ_base['HTTP_ACCEPT'] = 'text/html'
        response = client.post('/handle_password', data=data)
        assert response.status_code == 200
        assert 'password_link' in str(response.data)
