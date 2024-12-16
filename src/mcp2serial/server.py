from typing import Any, Optional, Tuple, Dict, List
import asyncio
import serial
import serial.tools.list_ports
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import logging
import yaml
import os
from dataclasses import dataclass, field
import time

# 设置日志级别为 DEBUG
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别以显示更多信息
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加版本号常量
VERSION = "0.1.0"  # 添加了自动\r\n和更详细的错误信息

server = Server("mcp2serial")

@dataclass
class Command:
    """Configuration for a serial command."""
    command: str
    need_parse: bool
    prompts: List[str]

@dataclass
class Config:
    """Configuration for MCP2Serial service."""
    port: Optional[str] = None
    baud_rate: int = 115200
    timeout: float = 1.0
    read_timeout: float = 1.0
    commands: Dict[str, Command] = field(default_factory=dict)

    @staticmethod
    def load(config_path: str = "config.yaml") -> 'Config':
        """Load configuration from YAML file."""
        # 定义可能的配置文件位置
        config_paths = [
            config_path,  # 首先检查指定的路径
            os.path.join(os.getcwd(), "config.yaml"),  # 当前工作目录
            os.path.expanduser("~/.mcp2serial/config.yaml"),  # 用户主目录
        ]
        
        # 添加系统级目录
        if os.name == 'nt':  # Windows
            config_paths.append(os.path.join(os.environ.get("ProgramData", "C:\\ProgramData"),
                                           "mcp2serial", "config.yaml"))
        else:  # Linux/Mac
            config_paths.append("/etc/mcp2serial/config.yaml")

        # 尝试从每个位置加载配置
        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                    logger.info(f"Loading configuration from {path}")
                    
                    # Load serial configuration
                    serial_config = config_data.get('serial', {})
                    config = Config(
                        port=serial_config.get('port'),
                        baud_rate=serial_config.get('baud_rate', 115200),
                        timeout=serial_config.get('timeout', 1.0),
                        read_timeout=serial_config.get('read_timeout', 1.0)
                    )

                    # Load commands
                    commands_data = config_data.get('commands', {})
                    for cmd_id, cmd_data in commands_data.items():
                        raw_command = cmd_data.get('command', '')
                        logger.debug(f"Loading command {cmd_id}: {repr(raw_command)}")
                        config.commands[cmd_id] = Command(
                            command=raw_command,
                            need_parse=cmd_data.get('need_parse', False),
                            prompts=cmd_data.get('prompts', [])
                        )
                        logger.debug(f"Loaded command {cmd_id}: {repr(config.commands[cmd_id].command)}")

                    return config
                except Exception as e:
                    logger.warning(f"Error loading config from {path}: {e}")
                    continue

        logger.info("No valid config file found, using defaults")
        return Config()

config = Config.load()

class SerialConnection:
    """Serial port connection manager."""
    
    def __init__(self):
        self.serial_port: Optional[serial.Serial] = None
        self.baud_rate: int = config.baud_rate
        self.timeout: float = 2.0  # 最大超时2秒
        self.read_timeout: float = 1.0

    def connect(self) -> bool:
        """Attempt to connect to an available serial port."""
        try:
            # 如果已经连接，直接返回
            if self.serial_port and self.serial_port.is_open:
                logger.debug("Using existing serial connection")
                return True

            # 关闭可能存在的连接
            if self.serial_port:
                try:
                    self.serial_port.close()
                except:
                    pass
                self.serial_port = None

            # 尝试连接指定端口
            if config.port:
                logger.info(f"Attempting to connect to configured port: {config.port}")
                try:
                    self.serial_port = serial.Serial(
                        port=config.port,
                        baudrate=self.baud_rate,
                        timeout=self.timeout
                    )
                    logger.info(f"Connected to configured port: {config.port}")
                    return True
                except serial.SerialException as e:
                    logger.error(f"Failed to connect to configured port {config.port}: {str(e)}")
                    raise ValueError(f"Serial port {config.port} not available: {str(e)}")

            # 搜索可用端口
            logger.info("No port configured, searching for available ports...")
            ports = list(serial.tools.list_ports.comports())
            if not ports:
                logger.error("No serial ports found")
                raise ValueError("No serial ports available")

            logger.info(f"Found ports: {', '.join(p.device for p in ports)}")
            for port in ports:
                try:
                    self.serial_port = serial.Serial(
                        port=port.device,
                        baudrate=self.baud_rate,
                        timeout=self.timeout
                    )
                    logger.info(f"Connected to port: {port.device}")
                    return True
                except serial.SerialException:
                    continue

            raise ValueError("Failed to connect to any available serial port")

        except Exception as e:
            logger.error(f"Unexpected error in connect: {str(e)}")
            raise ValueError(f"Connection error: {str(e)}")

    def send_command(self, command: Command, arguments: Dict[str, Any]) -> list[types.TextContent]:
        """Send a command to the serial port and return result according to MCP protocol."""
        try:
            # 确保连接
            if not self.serial_port or not self.serial_port.is_open:
                logger.info("No active connection, attempting to connect...")
                if not self.connect():
                    error_msg = f"[MCP2Serial v{VERSION}] Failed to establish serial connection.\n"
                    error_msg += "Please check:\n"
                    error_msg += "1. Serial port is correctly configured in config.yaml\n"
                    error_msg += "2. Device is properly connected\n"
                    error_msg += "3. No other program is using the port"
                    return [types.TextContent(
                        type="text",
                        text=error_msg
                    )]

            # 准备命令
            cmd_str = command.command.format(**arguments)
            # 确保命令以\r\n结尾
            cmd_str = cmd_str.rstrip() + '\r\n'  # 移除可能的空白字符，强制添加\r\n
            cmd_bytes = cmd_str.encode()
            logger.info(f"Sending command: {cmd_str.strip()}")
            logger.info(f"Command bytes ({len(cmd_bytes)} bytes): {' '.join([f'0x{b:02X}' for b in cmd_bytes])}")

            # 清空缓冲区
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()

            # 发送命令
            bytes_written = self.serial_port.write(cmd_bytes)
            logger.info(f"Wrote {bytes_written} bytes")
            self.serial_port.flush()

            # 等待一段时间确保命令被处理
            time.sleep(0.1)

            # 读取所有响应
            responses = []
            while self.serial_port.in_waiting:
                response = self.serial_port.readline()
                logger.info(f"Raw response: {response}")
                if response:
                    responses.append(response)

            if not responses:
                logger.error("No response received within timeout")
                error_msg = f"[MCP2Serial v{VERSION}] Command timeout - no response within {self.read_timeout} second(s)\n"
                error_msg += f"Command sent: {cmd_str.strip()}\n"
                error_msg += f"Command bytes ({len(cmd_bytes)} bytes): {' '.join([f'0x{b:02X}' for b in cmd_bytes])}\n"
                error_msg += "Please check:\n"
                error_msg += "1. Device is powered and responding\n"
                error_msg += "2. Baud rate matches device settings\n"
                error_msg += "3. Serial connection is stable\n"
                return [types.TextContent(
                    type="text",
                    text=error_msg
                )]

            # 解码第一行响应
            first_response = responses[0]
            first_line = first_response.decode().strip()
            logger.info(f"Decoded first response: {first_line}")

            # 检查是否有第二行响应
            if len(responses) > 1:
                second_response = responses[1]
                if second_response.startswith(b"OK"):
                    if command.need_parse:
                        return [types.TextContent(
                            type="text",
                            text=second_response.decode().strip()
                        )]
                    return []

            # 如果响应不是预期的格式，返回详细的错误信息
            error_msg = f"[MCP2Serial v{VERSION}] Command execution failed.\n"
            error_msg += f"Command sent: {cmd_str.strip()}\n"
            error_msg += f"Command bytes ({len(cmd_bytes)} bytes): {' '.join([f'0x{b:02X}' for b in cmd_bytes])}\n"
            error_msg += "Responses received:\n"
            for i, resp in enumerate(responses, 1):
                error_msg += f"{i}. Raw: {resp!r}\n   Decoded: {resp.decode().strip()}\n"
            error_msg += "\nPossible reasons:\n"
            error_msg += "- Device echoed the command but did not send OK response\n"
            error_msg += "- Command format may be incorrect\n"
            error_msg += "- Device may be in wrong mode\n"
            return [types.TextContent(
                type="text",
                text=error_msg
            )]

        except serial.SerialTimeoutException as e:
            logger.error(f"Serial timeout: {str(e)}")
            error_msg = f"[MCP2Serial v{VERSION}] Command timeout - {str(e)}\n"
            error_msg += "Please check:\n"
            error_msg += "1. Device is powered and responding\n"
            error_msg += "2. Baud rate matches device settings\n"
            error_msg += "3. Device is not busy with other operations"
            return [types.TextContent(
                type="text",
                text=error_msg
            )]
        except serial.SerialException as e:
            logger.error(f"Serial error: {str(e)}")
            error_msg = f"[MCP2Serial v{VERSION}] Serial communication failed - {str(e)}\n"
            error_msg += "Please check:\n"
            error_msg += "1. Serial port is correctly configured in config.yaml\n"
            error_msg += "2. Device is properly connected\n"
            error_msg += "3. No other program is using the port"
            return [types.TextContent(
                type="text",
                text=error_msg
            )]
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            error_msg = f"[MCP2Serial v{VERSION}] Internal error - {str(e)}\n"
            error_msg += "Please check:\n"
            error_msg += "1. Configuration is correct\n"
            error_msg += "2. Device is functioning properly"
            return [types.TextContent(
                type="text",
                text=error_msg
            )]

    def close(self) -> None:
        """Close the serial port connection if open."""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
                logger.info(f"Closed serial port connection: {self.serial_port.port}")
            except Exception as e:
                logger.error(f"Error closing port: {str(e)}")
            self.serial_port = None

serial_connection = SerialConnection()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for the MCP service."""
    logger.info("Listing available tools")
    tools = []
    
    for cmd_id, command in config.commands.items():
        # 从命令字符串中提取参数名
        import re
        param_names = re.findall(r'\{(\w+)\}', command.command)
        properties = {name: {"type": "string"} for name in param_names}
        
        tools.append(types.Tool(
            name=cmd_id,
            description=f"Execute {cmd_id} command",
            inputSchema={
                "type": "object",
                "properties": properties,
                "required": param_names
            },
            prompts=command.prompts
        ))
    
    return tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
    """Handle tool execution requests according to MCP protocol."""
    logger.info(f"Tool call received - Name: {name}, Arguments: {arguments}")
    
    try:
        if name not in config.commands:
            error_msg = f"[MCP2Serial v{VERSION}] Error: Unknown tool '{name}'\n"
            error_msg += "Please check:\n"
            error_msg += "1. Tool name is correct\n"
            error_msg += "2. Tool is configured in config.yaml"
            return [types.TextContent(
                type="text",
                text=error_msg
            )]

        command = config.commands[name]
        if arguments is None:
            arguments = {}
        
        # 发送命令并返回 MCP 格式的响应
        return serial_connection.send_command(command, arguments)

    except Exception as e:
        logger.error(f"Error handling tool call: {str(e)}")
        error_msg = f"[MCP2Serial v{VERSION}] Error: {str(e)}\n"
        error_msg += "Please check:\n"
        error_msg += "1. Configuration is correct\n"
        error_msg += "2. Device is functioning properly"
        return [types.TextContent(
            type="text",
            text=error_msg
        )]

async def main():
    """Run the MCP server."""
    logger.info("Starting MCP2Serial server")
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp2serial",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        serial_connection.close()

if __name__ == "__main__":
    asyncio.run(main())
