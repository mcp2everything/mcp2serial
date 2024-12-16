# MCP2Serial: Bridge between AI Models and Physical World

Connect AI Large Language Models to hardware devices through the Model Context Protocol (MCP).

[GitHub Repository](https://github.com/mcp2everything/mcp2serial) | [Documentation](https://github.com/mcp2everything/mcp2serial/tree/main/docs)

## Features

- **Intelligent Serial Communication**
  - Automatic port detection and configuration
  - Multiple baud rate support (default 115200)
  - Real-time status monitoring and error handling

- **PWM Control**
  - Precise frequency control (0-100Hz)
  - Real-time feedback
  - Multi-channel support

- **MCP Protocol Integration**
  - Full Model Context Protocol support
  - Resource management and tool invocation
  - Flexible prompt system

## Supported Clients

MCP2Serial supports all clients implementing the MCP protocol, including:

- Claude Desktop (Full support)
- Continue (Full support)
- Cline (Resource + Tools)
- Zed (Basic support)
- Sourcegraph Cody (Resource support)
- Firebase Genkit (Partial support)

## Quick Start

```bash
# Install using uv (recommended)
uv pip install mcp2serial

# Or using traditional pip
pip install mcp2serial
```

## Basic Configuration

Add the following to your MCP client configuration:

```json
{
    "mcpServers": {
        "mcp2serial": {
            "command": "uv",
            "args": [
                "--directory",
                "your_actual_path/mcp2serial",
                "run",
                "mcp2serial"
            ]
        }
    }
}
```

## Serial Port Configuration

Create or modify `config.yaml` to configure serial port parameters:

```yaml
serial:
  port: COM11  # Windows example, on Linux might be /dev/ttyUSB0
  baud_rate: 115200  # Baud rate
  timeout: 1.0  # Serial timeout (seconds)
  read_timeout: 0.5  # Read timeout (seconds)
```

If `port` is not specified, the program will automatically search for available serial ports.

## Configuration File Location

The configuration file (`config.yaml`) can be placed in several locations. The program will search for it in the following order:

1. Current working directory: `./config.yaml`
2. User's home directory: `~/.mcp2serial/config.yaml`
3. System-wide configuration:
   - Windows: `C:\ProgramData\mcp2serial\config.yaml`
   - Linux/Mac: `/etc/mcp2serial/config.yaml`

The first valid configuration file found will be used.

## Serial Port Configuration

Create a `config.yaml` file in one of the above locations with the following structure:

```yaml
serial:
  port: COM11  # or /dev/ttyUSB0 for Linux
  baud_rate: 115200
  timeout: 1.0
  read_timeout: 0.5

commands:
  # Add your commands here
  # See the Command Configuration section for examples
```

## Command Configuration

Add custom commands in `config.yaml`:

```yaml
commands:
  # PWM control command example
  set_pwm:
    command: "PWM {frequency}\n"  # Actual command format to send
    need_parse: false  # No need to parse response
    prompts:  # Prompt list
      - "Set PWM to {value}"
      - "Turn off PWM"

  # LED control command example
  led_control:
    command: "LED {state}\n"  # state can be on/off or other values
    need_parse: false
    prompts:
      - "Turn on LED"
      - "Turn off LED"
      - "Set LED state to {state}"

  # Command example with response parsing
  get_sensor:
    command: "GET_SENSOR\n"
    need_parse: true  # Need to parse response
    prompts:
      - "Read sensor data"
```

### Response Parsing

1. Simple Response (`need_parse: false`):
   - Device returns message starting with "OK" indicates success
   - Other responses will be treated as errors

2. Parsed Response (`need_parse: true`):
   - Complete response will be returned in the `result.raw` field

## Documentation

For detailed documentation, please visit our [GitHub repository](https://github.com/mcp2everything/mcp2serial).

## Support

If you encounter any issues or have questions:
1. Check our [Issues](https://github.com/mcp2everything/mcp2serial/issues) page
2. Read our [Wiki](https://github.com/mcp2everything/mcp2serial/wiki)
3. Create a new issue if needed

## License

This project is licensed under the MIT License.
