import pytest
from unittest.mock import Mock, patch
from mcp2serial.serial_handler import SerialHandler

def test_serial_connection():
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value.is_open = True
        handler = SerialHandler('COM1', 115200)
        assert handler.is_connected()

def test_pwm_frequency_validation():
    with patch('serial.Serial') as mock_serial:
        handler = SerialHandler('COM1', 115200)
        
        # Test valid frequency
        assert handler.validate_frequency(50) is True
        
        # Test invalid frequencies
        assert handler.validate_frequency(-1) is False
        assert handler.validate_frequency(101) is False
        assert handler.validate_frequency("not a number") is False
