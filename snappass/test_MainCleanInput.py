import pytest
from main import clean_input
from flask import request
from unittest.mock import patch

class Test_MainCleanInput:

    @pytest.mark.parametrize("form_data", [{"ttl": "hour"}, {}])
    def test_empty_password(self, form_data):
        with patch.object(request, 'form', form_data):
            with pytest.raises(Exception) as execinfo:
                clean_input()
                assert execinfo.type is 400

    @pytest.mark.parametrize("form_data", [{"password": "pass123"}, {}])
    def test_empty_ttl(self, form_data):
        with patch.object(request, 'form', form_data):
            with pytest.raises(Exception) as execinfo:
                clean_input()
                assert execinfo.type is 400

    @pytest.mark.parametrize("form_data", [{"password": "pass123", "ttl": "not_in_time_conversion"}])
    def test_invalid_ttl_value(self, form_data):
        with patch.object(request, 'form', form_data):
            with pytest.raises(Exception) as execinfo:
                clean_input()
                assert execinfo.type is 400

    @pytest.mark.parametrize("form_data", [{"password": "pass123", "ttl": "hour"}])
    def test_all_valid_params(self, form_data, TIME_CONVERSION={"hour": 3600}):
        with patch.object(request, 'form', form_data):
            result = clean_input()
            assert result == (TIME_CONVERSION[form_data["ttl"]], form_data["password"])
 