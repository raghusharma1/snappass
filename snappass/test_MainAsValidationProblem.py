import pytest
from main import as_validation_problem
from flask import Flask, Request
from werkzeug.exceptions import BadRequest

# Initialize flask app for testing
app = Flask(__name__)

class Test_MainAsValidationProblem:
    
    @pytest.fixture
    def request_obj(self):
        # Create a fixture for request object 
        with app.test_request_context('http://localhost/'):
            yield Request

    @pytest.mark.regression
    @pytest.mark.positive
    def test_as_validation_problem_success(self, request_obj):
        response = as_validation_problem(request_obj, "test_problem", "Test Problem", {"arg1": "arg2"})
        assert response["type"] == "http://localhost/test_problem"
        assert response["title"] == "Test Problem"
        assert response["invalid-params"] == {"arg1": "arg2"}

    @pytest.mark.negative
    def test_as_validation_problem_connection_failure(self):
        # create an invalid request for test
        with pytest.raises(Exception):
            with app.test_request_context('http://localhostinvalid/'):
                request = Request
                as_validation_problem(request, "test_problem", "Test Problem", {"arg1": "arg2"})

    @pytest.mark.negative
    def test_as_validation_problem_invalid_problem_type(self, request_obj):
        with pytest.raises(BadRequest):
            as_validation_problem(request_obj, "", "Test Problem", {"arg1": "arg2"})
    

    @pytest.mark.regression
    @pytest.mark.positive
    def test_as_validation_problem_no_trailing_slash(self, request_obj):
        response = as_validation_problem(request_obj, "test_problem", "Test Problem", {"arg1": "arg2"})
        assert response["type"] == "http://localhost/test_problem"
