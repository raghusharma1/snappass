import pytest
import os
from flask import Flask, jsonify, request
from main import api_handle_password
from fakeredis import FakeStrictRedis
from distutils.util import strtobool

app = Flask(__name__)

def set_password(password, ttl):
    # TODO: define this helper function

def set_base_url(request):
    # TODO: define this helper function

def test_api_handle_password_valid_inputs():
    with app.test_request_context():
        request.json = {'password': 'securepassword', 'ttl': 86400}
        response = api_handle_password()
        assert response.status_code == 200
        assert 'link' in response.json
        assert response.json['ttl'] == request.json['ttl']

def test_api_handle_password_no_password():
    with app.test_request_context():
        request.json = {'ttl': 86400}
        response = api_handle_password()
        assert response.status_code == 500

def test_api_handle_password_large_ttl():
    MAX_TTL = 1209600
    with app.test_request_context():
        request.json = {'password': 'securepassword', 'ttl': MAX_TTL + 1}
        response = api_handle_password()
        assert response.status_code == 500

def test_api_handle_password_no_ttl():
    DEFAULT_API_TTL = 1209600
    with app.test_request_context():
        request.json = {'password': 'securepassword'}
        response = api_handle_password()
        assert response.status_code == 200
        assert 'link' in response.json
        assert response.json['ttl'] == DEFAULT_API_TTL
