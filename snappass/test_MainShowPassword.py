import pytest
import redis
from unittest.mock import patch, MagicMock
from flask import render_template
from main import show_password
from redis.exceptions import ConnectionError

# Test Class
class Test_MainShowPassword:
  
    # Scenario 1: Testing the show_password when invalid key is provided
    @patch("main.get_password")
    def test_show_password_invalid_key(self, mock_get_password):
        # Arrange
        invalid_key = 'invalid'
        mock_get_password.return_value = None

        # Act
        response = show_password(invalid_key)

        # Assert
        assert response == (render_template('expired.html'), 404)

    # Scenario 2: Testing the show_password for valid key
    @patch("main.get_password")
    def test_show_password_valid_key(self, mock_get_password):
        # Arrange
        valid_key = 'valid'
        valid_password = 'valid_password'
        mock_get_password.return_value = valid_password

        # Act
        response = show_password(valid_key)

        # Assert
        assert response == render_template('password.html', password=valid_password)

    # Scenario 3: Testing the show_password function behavior when Redis server encounters a connection error
    @patch("main.get_password", side_effect=ConnectionError)
    def test_show_password_redis_error(self, mock_get_password):
        # Arrange
        password_key = 'key'
        expected_err_msg = 'Failed to connect to Redis server'

        # Act
        with pytest.raises(Exception) as e_info:
            show_password(password_key)

        # Assert
        assert str(e_info.value) == expected_err_msg
