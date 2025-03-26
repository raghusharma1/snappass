import pytest
from cryptography.fernet import Fernet, InvalidToken
from main import decrypt

def test_decrypt_valid_password():
    password = b'TestPassword123'
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password)
    
    assert decrypt(encrypted_password, key) == password

def test_decrypt_invalid_key():
    password = b'Test123'
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password)

    invalid_key = Fernet.generate_key()

    with pytest.raises(InvalidToken):
        decrypt(encrypted_password, invalid_key)

def test_decrypt_empty_or_none_password():
    key = Fernet.generate_key()
    
    with pytest.raises(InvalidToken):
        decrypt(None, key)

    with pytest.raises(InvalidToken):
        decrypt('', key)

def test_decrypt_badly_formatted_password():
    key = Fernet.generate_key()

    with pytest.raises(TypeError):
        decrypt('incorrectformat', key)

    with pytest.raises(TypeError):
        decrypt(12345, key)
