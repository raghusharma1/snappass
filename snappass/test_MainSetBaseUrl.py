import os
import pytest
from flask import Flask, Request
from unittest.mock import patch
from main import set_base_url

class Test_MainSetBaseUrl:

    @pytest.fixture
    def mock_request(self):
        app = Flask(__name__)
        with app.test_request_context('http://example.com/'):
            yield Request

    # Scenario 1
    @patch.dict(os.environ, {"NO_SSL": "True", "HOST_OVERRIDE": ""})
    def test_set_base_url_without_ssl_and_host_override(self, mock_request):
        base_url = set_base_url(mock_request)
        assert base_url == "http://example.com/"

    # Scenario 2
    @patch.dict(os.environ, {"NO_SSL": "False", "HOST_OVERRIDE": ""})
    def test_set_base_url_with_ssl_and_without_host_override(self, mock_request):
        base_url = set_base_url(mock_request)
        assert base_url == "https://example.com/"

    # Scenario 3
    @patch.dict(os.environ, {"NO_SSL": "True", "HOST_OVERRIDE": "override.host"})
    def test_set_base_url_without_ssl_and_with_host_override(self, mock_request):
        base_url = set_base_url(mock_request)
        assert base_url == "http://override.host/"

    # Scenario 4
    @patch.dict(os.environ, {"NO_SSL": "True", "HOST_OVERRIDE": "", "URL_PREFIX": "prefix"})
    def test_set_base_url_with_url_prefix(self, mock_request):
        base_url = set_base_url(mock_request)
        assert base_url == "http://example.com/prefix/"

    @patch.dict(os.environ, {"NO_SSL": "True", "HOST_OVERRIDE": "", "URL_PREFIX": "/prefix/"})
    def test_set_base_url_with_url_prefix_and_slashes(self, mock_request):
        base_url = set_base_url(mock_request)
        assert base_url == "http://example.com/prefix/"
