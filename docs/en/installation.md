# MCP2Serial Installation Guide

## Requirements

- Python 3.11 or higher
- uv package manager
- Serial device (e.g., Arduino, Raspberry Pi Pico)

## Installation Steps

1. Clone the repository:

```bash
# Clone the repository
git clone https://github.com/mcp2everything/mcp2serial.git
```

2. Create and activate virtual environment:

```bash
# Navigate to project directory
cd mcp2serial

# Create virtual environment using uv
uv venv .venv
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

> **Note:** The project will be available on PyPI soon, enabling direct installation via pip.

## Running the Server

```bash
# Ensure you're in the project root
cd mcp2serial

# Activate virtual environment (if not already activated)
.venv\Scripts\activate

# Run the server
uv run src/mcp2serial/server.py
```

## Configuration

### Configuration File Location

The configuration file (`config.yaml`) can be placed in several locations. The program will search for it in the following order:

1. Current working directory: `./config.yaml`
2. User's home directory: `~/.mcp2serial/config.yaml`
3. System-wide configuration:
   - Windows: `C:\ProgramData\mcp2serial\config.yaml`
   - Linux/Mac: `/etc/mcp2serial/config.yaml`

The first valid configuration file found will be used.

### Serial Port Configuration

Configure serial port parameters in `config.yaml`:

```yaml
serial:
  port: COM11  # Example for Windows, might be /dev/ttyUSB0 on Linux
  baud_rate: 115200  # Baud rate
  timeout: 1.0  # Serial timeout in seconds
  read_timeout: 0.5  # Read timeout in seconds
```

### MCP Client Configuration

When using MCP protocol-compatible clients (like Claude Desktop or Cline), add the following to your client's configuration file:

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
    <img src="../images/client_config.png" alt="Client Configuration Example" width="600"/>
    <p>Configuration Example in Claude Desktop</p>
</div>

<div align="center">
    <img src="../images/cline_config.png" alt="Cline Configuration Example" width="600"/>
    <p>Configuration Example in Cline</p>
</div>

> **Important Notes:**
> 1. Use absolute paths only
> 2. Use forward slashes (/) or double backslashes (\\) as path separators
> 3. Ensure the path points to your actual project installation directory

### Verifying Configuration

Run the following test command to verify your configuration:

```bash
uv run python tests/test_basic_serial.py
```

If configured correctly, you should see output similar to this:

<div align="center">
    <img src="../images/test_output.png" alt="Test Output Example" width="600"/>
    <p>Test Command Output Example</p>
</div>

## Troubleshooting

1. Serial Port Issues:
   - Ensure the device is properly connected
   - Verify the correct COM port in Device Manager
   - Check baud rate settings match your device

2. MCP Client Issues:
   - Verify the path in configuration is absolute and correct
   - Ensure uv is installed and in system PATH
   - Check if virtual environment is activated

3. Communication Issues:
   - Monitor the serial output for debugging
   - Check device response format
   - Verify command syntax in config.yaml
