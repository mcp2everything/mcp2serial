from typing import Any, Optional, Tuple
import asyncio
import serial
import serial.tools.list_ports
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import logging

# 设置更详细的日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

server = Server("mcp2serial")

class SerialConnection:
    """Serial port connection manager for PWM control."""
    
    def __init__(self):
        self.serial_port: Optional[serial.Serial] = None
        self.baud_rate: int = 115200
        self.timeout: float = 1.0

    def connect(self) -> bool:
        """Attempt to connect to an available serial port."""
        if self.serial_port and self.serial_port.is_open:
            logger.info(f"Already connected to serial port: {self.serial_port.port}")
            return True
            
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            logger.warning("No serial ports found")
            return False

        logger.info(f"Found {len(ports)} serial ports: {', '.join(p.device for p in ports)}")
        
        for port in ports:
            try:
                self.serial_port = serial.Serial(
                    port=port.device,
                    baudrate=self.baud_rate,
                    timeout=self.timeout
                )
                logger.info(f"Successfully connected to serial port: {port.device} (Description: {port.description})")
                return True
            except serial.SerialException as e:
                logger.warning(f"Failed to connect to {port.device}: {str(e)}")
                continue
        return False

    def send_pwm(self, frequency: int) -> Tuple[bool, str]:
        """Send PWM command to the serial port.
        
        Args:
            frequency: Integer between 0 and 100 representing PWM frequency
            
        Returns:
            Tuple of (success, message)
        """
        if not 0 <= frequency <= 100:
            logger.error(f"Invalid frequency value: {frequency}")
            return False, "Frequency must be between 0 and 100"

        if not self.connect():
            logger.error("Failed to connect to any serial port")
            return False, "No available serial port found"

        try:
            command = f"PWM {frequency}\n"
            logger.info(f"Sending command: {command.strip()}")
            self.serial_port.write(command.encode())
            
            response = self.serial_port.readline().decode().strip()
            logger.info(f"Received response: {response}")

            if response == "OK":
                logger.info(f"Successfully set PWM frequency to {frequency}%")
                return True, "OK"
            logger.warning(f"Unexpected response from device: {response}")
            return False, f"Unexpected response: {response}"
        except serial.SerialException as e:
            error_msg = f"Serial communication error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def close(self) -> None:
        """Close the serial port connection if open."""
        if self.serial_port and self.serial_port.is_open:
            port_name = self.serial_port.port
            self.serial_port.close()
            logger.info(f"Closed serial port connection: {port_name}")

serial_connection = SerialConnection()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for the MCP service."""
    logger.info("Listing available tools")
    return [
        types.Tool(
            name="set-pwm",
            description="Set PWM frequency (0-100)",
            inputSchema={
                "type": "object",
                "properties": {
                    "frequency": {
                        "type": "integer",
                        "description": "PWM frequency (0-100)",
                        "minimum": 0,
                        "maximum": 100,
                    },
                },
                "required": ["frequency"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> Any:
    """Handle tool execution requests."""
    logger.info(f"Tool call received - Name: {name}, Arguments: {arguments}")
    
    if name == "set-pwm":
        if not arguments or "frequency" not in arguments:
            logger.error("Missing frequency parameter")
            return {"error": "Missing frequency parameter"}

        frequency = arguments["frequency"]
        logger.info(f"Setting PWM frequency to {frequency}%")
        
        success, message = serial_connection.send_pwm(frequency)
        
        if success:
            logger.info("PWM command completed successfully")
            return {"status": "success", "message": message}
        else:
            logger.error(f"PWM command failed: {message}")
            return {"error": message}
    else:
        logger.error(f"Unknown tool: {name}")
        return {"error": "Unknown tool"}

async def main() -> None:
    """Run the MCP server."""
    logger.info("Starting MCP2Serial server...")
    try:
        # Run the server using stdin/stdout streams
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("Initialized stdio server")
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
        logger.error(f"Server error: {str(e)}")
        raise
    finally:
        serial_connection.close()
        logger.info("Server shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())
