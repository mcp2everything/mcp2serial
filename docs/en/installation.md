# MCP2Serial Installation Guide

## Requirements

- Python 3.11 or higher
- uv package manager
- Serial device (e.g., Arduino, Raspberry Pi Pico)

## Installation Steps

1. Create and activate virtual environment:

```bash
# Navigate to project directory
cd mcp2serial

# Create virtual environment and install dependencies using uv
uv venv .venv
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

## Running the Server

```bash
# Make sure you're in the project root directory
cd mcp2serial

# Activate virtual environment (if not already activated)
.venv\Scripts\activate

# Run the server
uv run src/mcp2serial/server.py
```

## Configuration Guide

### Serial Port Configuration

Configure serial port parameters in `config.yaml`:

```yaml
serial:
  port: COM11  # Windows example, might be /dev/ttyUSB0 on Linux
  baud_rate: 115200  # Baud rate
  timeout: 1.0  # Serial timeout in seconds
  read_timeout: 0.5  # Read timeout in seconds
```

If `port` is not specified, the program will automatically search for available serial ports.

### Command Configuration

Add custom commands in `config.yaml`:

```yaml
commands:
  # PWM control command example
  set_pwm:
    command: "PWM {frequency}\n"  # Actual command format
    need_parse: false  # No response parsing needed
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
    need_parse: true  # Response needs parsing
    prompts:
      - "Read sensor data"
```

### Response Parsing Guide

1. Simple Response (`need_parse: false`):
   - Device response starting with "OK" indicates success
   - Other responses are treated as errors

2. Response Requiring Parsing (`need_parse: true`):
   - Complete response is returned in the `result.raw` field
   - Further parsing can be done at the application level

Response examples:
```python
# Simple response
{"status": "success"}

# Response requiring parsing
{"status": "success", "result": {"raw": "OK TEMP=25.5,HUMIDITY=60%"}}
```

## Troubleshooting

1. Serial Port Connection Issues:
   - Verify device connection
   - Check port number
   - Verify baud rate settings
   - Check port permissions (Linux systems)

2. Command Timeout:
   - Check `timeout` and `read_timeout` settings
   - Verify device response time

## Testing

Run test cases:

```bash
# Activate virtual environment (if not already activated)
.venv\Scripts\activate

# Run tests
uv run pytest tests/
```

## More Information

For detailed API documentation and examples, refer to the [API Documentation](../api.md).
