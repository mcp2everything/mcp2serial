# MCP2Serial Service

English | [简体中文](README.md)

<div align="center">
    <img src="docs/images/logo.png" alt="MCP2Serial Logo" width="200"/>
</div>

A Claude MCP protocol-based serial communication service for PWM frequency control.

## Features

- Auto-detect and connect to serial ports at 115200 baud rate
- Control PWM frequency (range: 0-100)
- Compliant with Claude MCP protocol
- Comprehensive error handling and status feedback
- Cross-platform support (Windows, Linux, macOS)

## Requirements

- Python 3.11+
- pyserial
- mcp

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp2serial.git
cd mcp2serial

# Install dependencies
uv pip install -e .
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

## Claude Configuration

Add the following configuration to your Claude config file:

```json
{
    "mcpServers": {
        "mcp2serial": {
            "command": "uv",
            "args": [
                "--directory",
                "C:\\path\\to\\mcp2serial",  // Use appropriate path format for your OS
                "run",
                "mcp2serial"
            ]
        }
    }
}
```

Note: Replace `C:\\path\\to\\mcp2serial` with the actual path to your installation.

For different operating systems:
- Windows: `C:\\path\\to\\mcp2serial`
- Linux/macOS: `/path/to/mcp2serial`

## Interacting with Claude

Once the service is running, you can control PWM through natural language conversations with Claude. Here are some example prompts:

- "Set PWM to 50%"
- "Turn PWM to maximum"
- "Turn off PWM output"
- "Adjust PWM frequency to 75%"
- "Can you set PWM to 25%?"

Claude will understand your intent and automatically invoke the appropriate commands. No need to remember specific command formats - just express your needs in natural language.

## API Reference

The service provides the following tool:

### set-pwm

Controls PWM frequency.

Parameters:
- `frequency`: Integer between 0 and 100
  - 0: Off
  - 100: Maximum output
  - Any value in between: Proportional output

Returns:
- Success: `{"status": "success", "message": "OK"}`
- Failure: `{"error": "error message"}`

Possible error messages:
- "Frequency must be between 0 and 100"
- "No available serial port found"
- "Serial communication error: ..."
- "Unexpected response: ..."

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

## License

[MIT](LICENSE)

## Acknowledgments

- Thanks to the [Claude](https://claude.ai) team for the MCP protocol
- [pySerial](https://github.com/pyserial/pyserial) for serial communication
- All contributors and users of this project

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/mcp2serial/issues) page
2. Read our [Wiki](https://github.com/yourusername/mcp2serial/wiki)
3. Create a new issue if needed
