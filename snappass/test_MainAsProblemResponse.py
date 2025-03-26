import pytest
from flask import jsonify, make_response
from main import as_problem_response


class Test_MainAsProblemResponse:

    @pytest.mark.parametrize('problem, status_code', [
        # Add more pairs problem: status_code if needed
        ('A generic problem', 500),
        ('Another problem', 404),
    ])
    def test_as_problem_response_status_code(self, problem, status_code):
        response = as_problem_response(problem, status_code)
        assert response.status_code == status_code
        assert response.json == problem
        assert response.headers['Content-Type'] == 'application/problem+json'

    def test_as_problem_response_without_status_code(self):
        problem = 'A problem without status code'
        response = as_problem_response(problem)
        assert response.status_code == 400
        assert response.json == problem
        assert response.headers['Content-Type'] == 'application/problem+json'

    @pytest.mark.parametrize('problem, status_code', [
        # Add more pairs problem: status_code if needed (status_code should not be int)
        ('A problem with invalid status code', 'five_hundred'),
        ('Another problem with invalid status code', None),
    ])
    def test_as_problem_response_invalid_status_code(self, problem, status_code):
        response = as_problem_response(problem, status_code)
        assert response.status_code == 400
        assert response.json == problem
        assert response.headers['Content-Type'] == 'application/problem+json'
        
    def test_as_problem_response_header(self):
        problem = "Testing header"
        status_code = 200
        response = as_problem_response(problem, status_code)
        assert response.headers['Content-Type'] == 'application/problem+json'
