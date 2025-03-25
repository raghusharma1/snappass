import os
import sys
import pytest
from unittest.mock import Mock
from redis.exceptions import ConnectionError

# Assuming the above function is part of a 'main' module
from main import check_redis_alive

class Test_MainCheckRedisAlive:

    # Scenario 1: Test when the function name is 'main' and the Redis is healthy.
    @pytest.mark.positive
    def test_main_with_healthy_redis(self):

        # Arrange
        mocked_main_func = Mock(__name__='main', return_value="PONG")
      
        # Act
        decorated_func = check_redis_alive(mocked_main_func)
      
        # Assert
        assert decorated_func() == "PONG"
      
    # Scenario 2: Test when the function name is 'main' and the Redis is unhealthy.
    @pytest.mark.negative
    def test_main_with_unhealthy_redis(self, capsys):

        # Arrange
        mocked_main_func = Mock(__name__='main', side_effect=ConnectionError('Error'))

        # Act
        decorated_func = check_redis_alive(mocked_main_func)
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            decorated_func()

        # Assert
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0
        captured = capsys.readouterr()
        assert 'Failed to connect to redis! Error' in captured.out


    # Scenario 3: Test when the function name is not 'main' and the Redis is unhealthy.
    @pytest.mark.negative
    def test_nonmain_with_unhealthy_redis(self):

        # Arrange
        mocked_not_main_func = Mock(__name__='not_main', side_effect=ConnectionError('Error'))

        # Act
        decorated_func = check_redis_alive(mocked_not_main_func)
        
        # Assert
        with pytest.raises(Exception) as excinfo:
            decorated_func()
        assert str(excinfo.value) == '500'

    # Scenario 4: Test when the function name is not 'main' and the Redis is healthy.
    @pytest.mark.positive
    def test_nonmain_with_healthy_redis(self):

        # Arrange
        mocked_not_main_func = Mock(__name__='not_main', return_value="PONG")
      
        # Act
        decorated_func = check_redis_alive(mocked_not_main_func)
      
        # Assert
        assert decorated_func() == "PONG"