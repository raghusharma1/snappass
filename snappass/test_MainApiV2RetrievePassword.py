import pytest
import main
from main import api_v2_retrieve_password
from unittest.mock import patch, MagicMock

class Test_MainApiV2RetrievePassword:

    @pytest.mark.valid
    def test_retrieve_password_valid_token(self):
        # Arrange
        valid_token = "test_token"
        expected_password = "test_password"
        with patch('main.get_password', return_value=expected_password) as mock_get_password:
            # Act
            result = api_v2_retrieve_password(valid_token)

        # Assert
        mock_get_password.assert_called_once_with(valid_token)
        assert result.json["password"] == expected_password

    @pytest.mark.invalid
    def test_retrieve_password_invalid_token(self):
        # Arrange
        invalid_token = "invalid_token"
        error_message = "The password doesn't exist."
        with patch('main.get_password', return_value=None) as mock_get_password:
            # Act
            result = api_v2_retrieve_password(invalid_token)

        # Assert
        mock_get_password.assert_called_once_with(invalid_token)
        assert result["detail"] == error_message

    @pytest.mark.invalid
    def test_retrieve_password_nonexistent_token(self):
        # Arrange
        nonexistent_token = "nonexistent_token"
        error_message = "The password doesn't exist."
        with patch('main.get_password', return_value=None) as mock_get_password:
            # Act
            result = api_v2_retrieve_password(nonexistent_token)

        # Assert
        mock_get_password.assert_called_once_with(nonexistent_token)
        assert result["detail"] == error_message

    @pytest.mark.valid
    @pytest.mark.negative
    def test_retrieve_password_case_sensitivity(self):
        # Arrange
        correct_case_token = "test_token"
        incorrect_case_token = "TEST_TOKEN"
        expected_password = "test_password"
        error_message = "The password doesn't exist."
        with patch('main.get_password', side_effect=[expected_password, None]) as mock_get_password:
            # Act
            correct_result = api_v2_retrieve_password(correct_case_token)
            incorrect_result = api_v2_retrieve_password(incorrect_case_token)

        # Assert
        assert mock_get_password.call_args_list == [correct_case_token, incorrect_case_token]
        assert correct_result.json["password"] == expected_password
        assert incorrect_result["detail"] == error_message

    @pytest.mark.invalid
    @pytest.mark.negative
    def test_retrieve_password_empty_token(self):
        # Arrange
        empty_token = ""
        error_message = "The password doesn't exist."
        with patch('main.get_password', return_value=None) as mock_get_password:
            # Act
            result = api_v2_retrieve_password(empty_token)

        # Assert
        mock_get_password.assert_called_once_with(empty_token)
        assert result["detail"] == error_message
