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

# 设置日志级别为 DEBUG
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别以显示更多信息
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        if not os.path.exists(config_path):
            logger.info(f"No config file found at {config_path}, using defaults")
            return Config()

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
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
                config.commands[cmd_id] = Command(
                    command=cmd_data.get('command', ''),
                    need_parse=cmd_data.get('need_parse', False),
                    prompts=cmd_data.get('prompts', [])
                )

            return config
        except Exception as e:
            logger.warning(f"Error loading config: {e}, using defaults")
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
                    raise ValueError("Failed to establish serial connection")

            # 准备命令
            cmd_str = command.command.format(**arguments)
            logger.info(f"Sending command: {cmd_str.strip()}")

            # 清空缓冲区
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()

            # 发送命令
            bytes_written = self.serial_port.write(cmd_str.encode())
            logger.info(f"Wrote {bytes_written} bytes")
            self.serial_port.flush()

            # 读取响应
            self.serial_port.timeout = self.read_timeout
            
            # 读取第一行响应
            first_response = self.serial_port.readline()
            logger.info(f"First line response: {first_response}")

            if not first_response:
                logger.error("No response received within timeout")
                return [types.TextContent(
                    type="text",
                    text="Error: Command timeout - no response within 1 second"
                )]

            # 解码第一行响应
            first_line = first_response.decode().strip()
            logger.info(f"Decoded first line: {first_line}")

            if first_response.startswith(b"OK"):
                if command.need_parse:
                    # 如果需要解析，继续读取剩余响应
                    full_response = [first_line]
                    while True:
                        line = self.serial_port.readline()
                        if not line:  # 如果没有更多数据，退出循环
                            break
                        decoded_line = line.decode().strip()
                        if decoded_line:  # 只添加非空行
                            full_response.append(decoded_line)
                    
                    # 返回完整响应
                    return [types.TextContent(
                        type="text",
                        text="\n".join(full_response)
                    )]
                return [types.TextContent(
                    type="text",
                    text="Command executed successfully"
                )]

            # 如果响应不是以 OK 开头，返回详细的错误信息
            error_msg = f"Command execution failed.\n"
            error_msg += f"Command sent: {cmd_str.strip()}\n"
            error_msg += f"Response received: {first_line}\n"
            error_msg += "Possible reasons:\n"
            
            if not first_response:
                error_msg += "- No response from device (timeout)\n"
                error_msg += "- Device not ready or busy\n"
            elif first_line == cmd_str.strip():
                error_msg += "- Device echoed the command but did not process it\n"
                error_msg += "- Command format may be incorrect\n"
            else:
                error_msg += "- Command not recognized by device\n"
                error_msg += "- Device in wrong state or mode\n"
            
            error_msg += "\nTroubleshooting steps:\n"
            error_msg += "1. Check if the device is properly connected and powered\n"
            error_msg += "2. Verify the command format in config.yaml\n"
            error_msg += "3. Make sure the device is in the correct mode to accept commands\n"
            
            return [types.TextContent(
                type="text",
                text=error_msg
            )]

        except serial.SerialTimeoutException as e:
            logger.error(f"Serial timeout: {str(e)}")
            return [types.TextContent(
                type="text",
                text=f"Error: Command timeout - {str(e)}"
            )]
        except serial.SerialException as e:
            logger.error(f"Serial error: {str(e)}")
            return [types.TextContent(
                type="text",
                text=f"Error: Serial communication failed - {str(e)}"
            )]
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return [types.TextContent(
                type="text",
                text=f"Error: Internal error - {str(e)}"
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
            return [types.TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]

        command = config.commands[name]
        if arguments is None:
            arguments = {}
        
        # 发送命令并返回 MCP 格式的响应
        return serial_connection.send_command(command, arguments)

    except Exception as e:
        logger.error(f"Error handling tool call: {str(e)}")
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
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
