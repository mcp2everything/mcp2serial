# MCP2Serial Service

English | [简体中文](README.md)

<div align="center">
    <img src="docs/images/logo.png" alt="MCP2Serial Logo" width="200"/>
</div>

MCP2Serial is a serial communication server based on the MCP service interface protocol, designed for communication with serial devices. It provides a simple configuration approach for defining and managing serial commands.

## Features

- 🔌 Automatic serial port detection and connection management
- 📝 Simple YAML configuration
- 🛠️ Customizable commands and response parsing
- 🌐 Multi-language prompt support
- 🚀 Asynchronous communication support
- Auto-detect and connect to serial ports at 115200 baud rate
- Control PWM frequency (range: 0-100)
- Compliant with Claude MCP protocol
- Comprehensive error handling and status feedback
- Cross-platform support (Windows, Linux, macOS)

## System Architecture

<div align="center">
    <img src="docs/images/stru_eng.png" alt="System Architecture" width="800"/>
    <p>MCP2Serial System Architecture</p>
</div>

## Workflow

<div align="center">
    <img src="docs/images/workflow_eng.png" alt="Workflow Diagram" width="800"/>
    <p>MCP2Serial Workflow Diagram</p>
</div>

## Quick Start

1. Install:
```bash
pip install mcp2serial
or
uv pip install mcp2serial
```

2. Configure serial port and commands:
```yaml
# config.yaml
serial:
  port: COM11  # or auto-detect
  baud_rate: 115200

commands:
  set_pwm:
    command: "PWM {frequency}\n"
    need_parse: false
    prompts:
      - "Set PWM to {value}%"
```


3.MCP json Configuration

Add the following to your MCP client (like Claude Desktop or Cline) configuration file, making sure to update the path to your actual installation path:

```json
{
    "mcpServers": {
        "mcp2serial": {
            "command": "uv",
            "args": [
                "--directory",
                "your_actual_path/mcp2serial",  // Example: "C:/Users/Administrator/Documents/develop/my-mcp-server/mcp2serial"
                "run",
                "mcp2serial"
            ]
        }
    }
}
```

<div align="center">
    <img src="docs/images/client_config.png" alt="Client Configuration Example" width="600"/>
    <p>Configuration Example in Claude Desktop</p>
</div>

<div align="center">
    <img src="docs/images/cline_config.png" alt="Cline Configuration Example" width="600"/>
    <p>Configuration Example in Cline</p>
</div>

> **Note:** The path must be an absolute path and use forward slashes (/) or double backslashes (\\) as path separators.

4. launch your client(claude desktop or cline):


## Interacting with Claude

Once the service is running, you can control PWM through natural language conversations with Claude. Here are some example prompts:

- "Set PWM to 50%"
- "Turn PWM to maximum"
- "Turn off PWM output"
- "Adjust PWM frequency to 75%"
- "Can you set PWM to 25%?"

Claude will understand your intent and automatically invoke the appropriate commands. No need to remember specific command formats - just express your needs in natural language.

<div align="center">
    <img src="docs/images/pwm.png" alt="Cline Configuration Example" width="600"/>
    <p> Example in Claude</p>
</div>
<div align="center">
    <img src="docs/images/test_output.png" alt="Cline Configuration Example" width="600"/>
    <p>Example in Cline</p>
</div>

## Documentation

- [Installation Guide](./docs/en/installation.md)
- [API Documentation](./docs/en/api.md)
- [Configuration Guide](./docs/en/configuration.md)

## Examples

### 1. Simple Command Configuration
```yaml
commands:
  led_control:
    command: "LED {state}\n"
    need_parse: false
    prompts:
      - "Turn on LED"
      - "Turn off LED"
```

### 2. Command with Response Parsing
```yaml
commands:
  get_temperature:
    command: "GET_TEMP\n"
    need_parse: true
    prompts:
      - "Get temperature"
```

Response example:
```python
{
    "status": "success",
    "result": {
        "raw": "OK TEMP=25.5"
    }
}
```

## Requirements

- Python 3.11+
- pyserial
- mcp

## Installation from source code
 
```bash
# source codeClone the repository
git clone https://github.com/mcp2everything/mcp2serial.git
cd mcp2serial
uv venv .venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

## Running the Service

Use the `uv run` command to automatically build, install, and run the service:

```bash
uv run src/mcp2serial/server.py
```

This command will:
1. Build the mcp2serial package
2. Install it in the current environment
3. Start the server


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   uv venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

### Running Tests

```bash
uv pytest tests/
```

## Project Roadmap

### Phase 1: Protocol Expansion
- **Industrial Protocol Support**
  - MODBUS RTU/TCP
  - OPC UA
  - MQTT
  - CoAP
  - TCP/IP Socket
  
- **Hardware Interface Extension**
  - I2C
  - SPI
  - CAN
  - 1-Wire
  - GPIO

### Phase 2: MCP2Anything Platform
- **Unified Integration Platform**
  - Visual Configuration Interface
  - One-Click Protocol Activation
  - Real-time Monitoring Dashboard
  - Device Management System

- **Intelligent Features**
  - Protocol Auto-Detection
  - Device Auto-Discovery
  - Parameter Smart Optimization
  - Anomaly Warning System

### Phase 3: Ecosystem Development
- **Plugin Marketplace**
  - Protocol Plugins
  - Device Drivers
  - Custom Function Modules
  - Community Contributions

- **Cloud Service Integration**
  - Device Cloud Management
  - Remote Control
  - Data Analytics
  - AI Training Platform

### Phase 4: Industry Solutions
- **Vertical Domain Adaptation**
  - Industrial Automation
  - Smart Buildings
  - Agricultural IoT
  - Smart Cities

- **Customization Services**
  - Industry Protocol Adaptation
  - Professional Technical Support
  - Solution Consulting
  - Training Services

## Vision & Future

MCP2Serial is revolutionizing IoT with:

- **Protocol Unification**: Complete protocol support through MCP2Anything platform
- **Plug and Play**: Zero-configuration setup with automatic discovery
- **AI Empowerment**: Deep AI integration for intelligent decision-making
- **Open Ecosystem**: Vibrant developer community and plugin marketplace

## License

[MIT](LICENSE)

## Acknowledgments

- Thanks to the [Claude](https://claude.ai) team for the MCP protocol
- [pySerial](https://github.com/pyserial/pyserial) for serial communication
- All contributors and users of this project

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/mcp2everything/mcp2serial/issues) page
2. Read our [Wiki](https://github.com/mcp2everything/mcp2serial/wiki)
3. Create a new issue if needed
