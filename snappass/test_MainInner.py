import os
import sys
import pytest
from main import inner
from unittest.mock import Mock, patch
from redis.exceptions import ConnectionError
from werkzeug.exceptions import HTTPException


class Test_MainInner:

    @pytest.mark.valid
    @patch('redis.StrictRedis')
    def test_main_connects_to_redis(self, mock_redis):
        mock_redis.ping.return_value = True
        mock_fn = Mock(__name__='main')
        inner_func = inner(mock_fn)

        assert inner_func()

    @pytest.mark.invalid
    @patch('sys.exit')
    @patch('redis.StrictRedis')
    def test_main_fails_to_connect_to_redis(self, mock_redis, mock_exit):
        mock_redis.ping.side_effect = ConnectionError
        mock_fn = Mock(__name__='main')
        inner_func = inner(mock_fn)

        with pytest.raises(SystemExit):
            inner_func()

    @pytest.mark.negative
    @patch('redis.StrictRedis')
    def test_not_main_fails_to_connect_to_redis(self, mock_redis):
        mock_redis.ping.side_effect = ConnectionError
        mock_fn = Mock(__name__='not_main')
        inner_func = inner(mock_fn)

        with pytest.raises(HTTPException) as e_info:
            inner_func()
        assert e_info.value.code == 500
