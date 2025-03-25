import pytest
#import all other required modules here
from main import api_v2_set_password

class Test_MainApiV2SetPassword:

    @pytest.mark.negative
    def test_password_not_provided(self, monkeypatch):
        def mock_get(*args, **kwargs):
            if 'password' in args:
                return None
            return 120
        monkeypatch.setattr('request.json.get', mock_get)
        resp = api_v2_set_password()
        assert "The password is required and should not be null or empty." in str(resp)

    @pytest.mark.negative
    def test_ttl_exceeds_maximum(self, monkeypatch):
        def mock_get(*args, **kwargs):
            if 'ttl' in args:
                return 121
            return "password"
        monkeypatch.setattr('request.json.get', mock_get)
        global MAX_TTL
        MAX_TTL = 120
        resp = api_v2_set_password()
        assert "The specified TTL is longer than the maximum supported." in str(resp)

    @pytest.mark.positive
    def test_successful_password_set(self, monkeypatch):
        def mock_get(*args, **kwargs):
            if 'ttl' in args:
                return 60
            return "password"
        monkeypatch.setattr('request.json.get', mock_get)
        predefined_token = "token"
        monkeypatch.setattr('set_password', lambda x, y: predefined_token)
        resp = api_v2_set_password()
        assert predefined_token in resp["token"]

    @pytest.mark.negative
    def test_invalid_request_form(self, monkeypatch):
        monkeypatch.setattr('request.json.get', lambda x: None)
        resp = api_v2_set_password()
        assert "The password and/or the TTL are invalid." in str(resp)
