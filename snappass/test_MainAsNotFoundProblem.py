import pytest
from main import as_not_found_problem
from flask import Flask
from flask.testing import FlaskClient
import random


class Test_MainAsNotFoundProblem:

    @pytest.fixture
    def client(self):
        flask_app = Flask(__name__)
        with flask_app.test_client() as client:
            yield client

    def test_as_not_found_problem_valid(self, client: FlaskClient):
        request = "/" + ''.join(random.choices('abcdef123456', k=10))
        problem_type = "/" + ''.join(random.choices('abcdef123456', k=10))
        problem_title = ''.join(random.choices('abcdef123456', k=10))
        invalid_params = [{'name': 'param1', 'reason': 'invalid'}]
        response = as_not_found_problem(client.get(request), problem_type, problem_title, invalid_params)
        assert response.status_code == 404
        assert response.get_json()["type"].endswith(problem_type)
        assert response.get_json()["title"] == problem_title
        assert response.get_json()["invalid-params"] == invalid_params

    def test_as_not_found_problem_invalid_request(self, client: FlaskClient):
        request = "/" + ''.join(random.choices('abcdef123456', k=10))
        problem_type = "/" + ''.join(random.choices('abcdef123456', k=10))
        problem_title = ''.join(random.choices('abcdef123456', k=10))
        invalid_params = [{'name': 'param1', 'reason': 'invalid'}]
        request = client.get(request)
        request.environ['REQUEST_URI'] = None
        with pytest.raises(Exception):
            as_not_found_problem(request, problem_type, problem_title, invalid_params)

    def test_as_not_found_problem_non_existing_type(self, client: FlaskClient):
        request = "/" + ''.join(random.choices('abcdef123456', k=10))
        problem_type = "/" + ''.join(random.choices('abcdef123456', k=10))
        problem_title = ''.join(random.choices('abcdef123456', k=10))
        invalid_params = [{'name': 'param1', 'reason': 'invalid'}]
        response = as_not_found_problem(client.get(request), problem_type, problem_title, invalid_params)
        assert response.status_code == 404
        assert response.get_json()["type"].endswith(problem_type)
        assert response.get_json()["title"] == problem_title
        assert response.get_json()["invalid-params"] == invalid_params

    def test_as_not_found_problem_empty_invalid_params(self, client: FlaskClient):
        request = "/" + ''.join(random.choices('abcdef123456', k=10))
        problem_type = "/" + ''.join(random.choices('abcdef123456', k=10))
        problem_title = ''.join(random.choices('abcdef123456', k=10))
        invalid_params = []
        response = as_not_found_problem(client.get(request), problem_type, problem_title, invalid_params)
        assert response.status_code == 404
        assert response.get_json()["type"].endswith(problem_type)
        assert response.get_json()["title"] == problem_title
        assert not response.get_json()["invalid-params"]
