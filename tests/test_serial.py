import pytest
import time
import logging
from typing import Dict, Any
from mcp2serial.server import SerialConnection, Config, Command, CommandResponse, CommandParameter, PromptTemplate
from mcp import types

# 设置日志级别为 DEBUG
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def config():
    """Load test configuration"""
    return Config.load("config.yaml")

@pytest.fixture
def serial_connection(config):
    """Create a serial connection using configuration"""
    connection = SerialConnection()
    yield connection
    connection.close()

def test_serial_connection(serial_connection):
    """Test connecting to the actual serial port"""
    assert serial_connection.connect() is True
    assert serial_connection.serial_port.is_open is True
    logger.info(f"Connected to port: {serial_connection.serial_port.port}")

def test_command_format(config):
    """Test command string formatting"""
    for cmd_id, command in config.commands.items():
        logger.info(f"Testing command format for {cmd_id}")
        try:
            # 准备测试参数
            test_args = {}
            for param in command.command.split("{")[1:]:
                param_name = param.split("}")[0]
                test_args[param_name] = "test"
            
            # 测试格式化
            formatted = command.command.format(**test_args)
            logger.info(f"Formatted command: {formatted}")
            assert len(formatted) > 0
            
        except Exception as e:
            pytest.fail(f"Command format error for {cmd_id}: {str(e)}")

def test_pico_info_command(serial_connection, config):
    """Test getting PICO board information with detailed logging"""
    logger.info("\nTesting PICO_INFO command")
    
    # 确保连接
    assert serial_connection.connect() is True
    
    # 获取命令配置
    command = config.commands['get_pico_info']
    logger.info(f"Command template: {command.command}")
    
    # 发送命令并记录原始响应
    response = serial_connection.send_command(command, {})
    assert isinstance(response, list), "Response should be a list"
    assert len(response) > 0, "Response should not be empty"
    
    # 记录每个响应内容
    for item in response:
        assert isinstance(item, types.TextContent), "Response item should be TextContent"
        logger.info(f"Response text: {item.text}")
        
        # 解析响应
        if item.text.startswith("Error:"):
            pytest.fail(f"Command failed: {item.text}")
            
    logger.info("PICO_INFO command test completed successfully")

def test_pwm_command(serial_connection, config):
    """Test sending PWM command with detailed logging"""
    logger.info("\nTesting PWM command")
    
    # 确保连接
    assert serial_connection.connect() is True
    
    # 获取命令配置
    command = config.commands['set_pwm']
    logger.info(f"Command template: {command.command}")
    
    # 测试不同的 PWM 值
    test_cases = [
        (0, "minimum"),
        (50, "half"),
        (100, "maximum")
    ]
    
    for frequency, description in test_cases:
        logger.info(f"\nTesting PWM {description}: {frequency}%")
        
        # 发送命令并记录响应
        response = serial_connection.send_command(command, {"frequency": str(frequency)})
        assert isinstance(response, list), "Response should be a list"
        assert len(response) > 0, "Response should not be empty"
        
        # 记录每个响应内容
        for item in response:
            assert isinstance(item, types.TextContent), "Response item should be TextContent"
            logger.info(f"Response text: {item.text}")
            
            # 检查错误
            if item.text.startswith("Error:"):
                pytest.fail(f"Command failed: {item.text}")
        
        time.sleep(1)  # 等待命令执行
        
    logger.info("PWM command test completed successfully")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
