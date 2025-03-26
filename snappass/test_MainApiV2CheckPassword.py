import pytest
from main import api_v2_check_password
from unittest.mock import patch

class Test_MainApiV2CheckPassword:

    @pytest.mark.positive
    @pytest.mark.valid
    @patch('main.password_exists')
    def test_api_v2_check_password_existing_token(self, password_exists_mock):
        
        # Arrange: Set return value for mocked function
        password_exists_mock.return_value = True
        test_token = "test_token"

        # Act:
        response = api_v2_check_password(test_token)

        # Assert:
        password_exists_mock.assert_called_once_with(test_token)
        assert response == ('', 200)


    @pytest.mark.negative
    @pytest.mark.valid
    @patch('main.password_exists')
    def test_api_v2_check_password_non_existing_token(self, password_exists_mock):

        # Arrange: Set return value for mocked function
        password_exists_mock.return_value = False
        test_token = "test_token"

        # Act:
        response = api_v2_check_password(test_token)

        # Assert:
        password_exists_mock.assert_called_once_with(test_token)
        assert response == ('', 404)


    @pytest.mark.negative
    @pytest.mark.invalid
    @patch('main.password_exists')
    def test_api_v2_check_password_invalid_token_format(self, password_exists_mock):

        # Arrange: Set return value for mocked function
        password_exists_mock.return_value = False
        test_token = "@invalid_token"
        
        # TODO: On the basis of the implementation specifics, replace the expected_response
        # with the expected return for an invalid token request.

        expected_response = ('', 400)

        # Act:
        response = api_v2_check_password(test_token)

        # Assert:
        password_exists_mock.assert_called_once_with(test_token)
        assert response == expected_response
