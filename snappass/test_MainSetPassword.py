import os
import pytest
import uuid
import redis
from unittest.mock import patch, Mock, call
from main import set_password
from cryptography.fernet import Fernet
from redis.exceptions import ConnectionError
from fakeredis import FakeStrictRedis

class Test_MainSetPassword:

    @patch('uuid.uuid4')
    @patch('main.redis_client')
    @patch('main.encrypt')
    def test_set_password_success(self, mock_encrypt, mock_redis_client, mock_uuid4):
        mock_uuid4.return_value.hex = 'random_hex'
        mock_encrypt.return_value = ('encrypted_password', b'encryption_key')
        password = 'test_password'
        ttl = 1209600
        expected_token = 'snappassrandom_hex~encryption_key'
        token = set_password(password, ttl)
        assert token == expected_token
        mock_redis_client.setex.assert_called_once_with('snappassrandom_hex', ttl, 'encrypted_password')

    @patch('uuid.uuid4')
    @patch('main.redis_client')
    @patch('main.encrypt')
    def test_password_encryption(self, mock_encrypt, mock_redis_client, mock_uuid4):
        mock_uuid4.return_value.hex = 'random_hex'
        password = 'test_password'
        ttl = 1209600
        set_password(password, ttl)
        mock_encrypt.assert_called_once_with('test_password')

    @patch('uuid.uuid4')
    @patch('main.redis_client')
    @patch('main.encrypt')
    def test_redis_connection_error(self, mock_encrypt, mock_redis_client, mock_uuid4):
        mock_uuid4.return_value.hex = 'random_hex'
        mock_encrypt.return_value = ('encrypted_password', b'encryption_key')
        password = 'test_password'
        ttl = 1209600
        mock_redis_client.setex.side_effect = ConnectionError
        with pytest.raises(ConnectionError):
            set_password(password, ttl)

    @patch('uuid.uuid4')
    @patch('main.redis_client')
    @patch('main.encrypt')
    def test_token_generation(self, mock_encrypt, mock_redis_client, mock_uuid4):
        mock_uuid4.return_value.hex = 'random_hex'
        mock_encrypt.return_value = ('encrypted_password', b'encryption_key')
        password = 'test_password'
        ttl = 1209600
        expected_token = 'snappassrandom_hex~encryption_key'
        token = set_password(password, ttl)
        assert TOKEN_SEPARATOR in token

    @patch('uuid.uuid4')
    @patch('main.redis_client')
    @patch('main.encrypt')
    def test_password_ttl(self, mock_encrypt, mock_redis_client, mock_uuid4):
        mock_uuid4.return_value.hex = 'random_hex'
        mock_encrypt.return_value = ('encrypted_password', b'encryption_key')
        password = 'test_password'
        ttl = 86400
        set_password(password, ttl)
        mock_redis_client.setex.assert_called_once_with('snappassrandom_hex', 86400, 'encrypted_password')
