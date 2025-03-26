import os
import pytest
import uuid
import redis
from cryptography.fernet import Fernet
from redis.exceptions import ConnectionError
from fakeredis import FakeStrictRedis
from main import get_password

class Test_MainGetPassword:
  
  @pytest.fixture
  def redis_fake(self, monkeypatch):
    """
    Use a fake Redis for tests.
    """
    fake_redis = FakeStrictRedis()
    monkeypatch.setattr('main.redis_client', fake_redis)
    return fake_redis  

  @pytest.fixture
  def decryption_key(self):
    """
    A valid decryption key
    """
    return Fernet.generate_key().decode()

  @pytest.fixture
  def storage_key(self):
    """
    A valid storage key
    """
    return str(uuid.uuid4())

  @pytest.mark.smoke
  def test_get_password_valid_token(self, redis_fake, decryption_key, storage_key):
    password = 'secret'
    redis_fake.set(storage_key, Fernet(decryption_key.encode()).encrypt(password.encode()))
    token = f'{storage_key}~{decryption_key}'
    assert get_password(token) == password

  @pytest.mark.regression
  def test_get_password_invalid_token(self, redis_fake, storage_key):
    password = 'secret'
    redis_fake.set(storage_key, password)
    token = f'{storage_key}~'
    assert get_password(token) == password

  @pytest.mark.regression
  def test_get_password_non_existent_key(self, decryption_key):
    storage_key = 'Non-existent'
    token = f'{storage_key}~{decryption_key}'
    assert get_password(token) is None

  @pytest.mark.regression
  def test_get_password_redis_error(self, monkeypatch, decryption_key, storage_key):
    def mock_get(*args, **kwargs):
      raise ConnectionError("Cannot connect to Redis")
    
    monkeypatch.setattr(redis.StrictRedis, "get", mock_get)
    token = f'{storage_key}~{decryption_key}'
    assert get_password(token) is None
