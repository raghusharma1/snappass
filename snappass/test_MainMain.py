import os
import pytest
import sys
import uuid
import redis
from cryptography.fernet import Fernet
from flask import abort, Flask, render_template, request, jsonify, make_response
from redis.exceptions import ConnectionError
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from urllib.parse import urljoin
from distutils.util import strtobool
from flask_babel import Babel
from fakeredis import FakeStrictRedis
from unittest.mock import patch, MagicMock
from main import main

class Test_MainMain:

    @pytest.mark.regression
    def test_main_default_values(self, monkeypatch):
        monkeypatch.delenv('SNAPPASS_BIND_ADDRESS', raising=False)
        monkeypatch.delenv('SNAPPASS_PORT', raising=False)

        with patch('flask.Flask.run') as mock_run:
            main()
            mock_run.assert_called_once_with(host='0.0.0.0', port=5000)

    @pytest.mark.regression
    def test_main_custom_values(self, monkeypatch):
        monkeypatch.setenv('SNAPPASS_BIND_ADDRESS', '127.0.0.1')
        monkeypatch.setenv('SNAPPASS_PORT', '6000')

        with patch('flask.Flask.run') as mock_run:
            main()
            mock_run.assert_called_once_with(host='127.0.0.1', port='6000')

    @pytest.mark.negative
    def test_main_connection_error(self, monkeypatch):
        mock_run = MagicMock()
        mock_run.side_effect = ConnectionError

        monkeypatch.setattr('flask.Flask.run', mock_run)

        with pytest.raises(ConnectionError):
            main()
