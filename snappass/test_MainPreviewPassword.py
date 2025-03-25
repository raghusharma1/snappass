import os
import flask
import pytest
from unittest.mock import patch, MagicMock
from urllib.parse import quote_plus, unquote_plus
from main import preview_password

@app.route('/test')
def test_end_point():
    return render_template('expired.html'), 404

def test_end_point():
    flask_client = app.test_client()
    response = flask_client.get('/test')
    assert response.status_code == 404

class Test_MainPreviewPassword:
    
    @pytest.mark.smoke
    @patch("main.password_exists", return_value=True)
    def test_valid_key(self, mock_password_exists):
        # Arrange
        password_key = "validPasswordKey"
        # Act
        resp = preview_password(password_key)
        # Assert
        assert mock_password_exists.called_once_with(password_key)
        assert resp[0] == render_template('preview.html')
        
    @pytest.mark.regression
    @patch("main.password_exists", return_value=False)
    def test_invalid_key(self, mock_password_exists):
        # Arrange
        password_key = "invalidPasswordKey"
        # Act
        resp = preview_password(password_key)
        # Assert
        assert mock_password_exists.called_once_with(password_key)
        assert resp == (render_template('expired.html'), 404)

    @pytest.mark.security
    @patch("main.password_exists", return_value=True)
    def test_url_encoding(self, mock_password_exists):
        # Arrange
        password_key = quote_plus("validPasswordKey")
        # Act
        resp = preview_password(password_key)
        # Assert
        password_key_decoded = unquote_plus(password_key)
        assert mock_password_exists.called_once_with(password_key_decoded)
        assert resp[0] == render_template('preview.html')
    
    @pytest.mark.negative
    @patch("main.password_exists", return_value=False)
    def test_empty_key(self, mock_password_exists):
        # Arrange
        password_key = ""
        # Act
        resp = preview_password(password_key)
        # Assert
        assert mock_password_exists.called_once_with(password_key)
        assert resp == (render_template('expired.html'), 404)
