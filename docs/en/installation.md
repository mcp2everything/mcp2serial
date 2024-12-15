# Installation Guide

## Prerequisites

- Python 3.11 or higher
- pip or uv package manager
- Serial port access rights (may require admin privileges on some systems)

## Installation Steps

### 1. Using pip

```bash
pip install mcp2serial
```

### 2. From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp2serial.git
cd mcp2serial

# Install in development mode
pip install -e .
```

## Configuration

### Serial Port Setup

The service automatically detects available serial ports. However, you can specify a particular port in the configuration:

1. Create a `config.yaml` in your working directory:
```yaml
serial:
  port: COM1  # Windows
  # port: /dev/ttyUSB0  # Linux
  # port: /dev/tty.usbserial-*  # macOS
  baud_rate: 115200
```

### Claude Integration

1. Add the following to your Claude configuration:
```json
{
    "mcpServers": {
        "mcp2serial": {
            "command": "uv",
            "args": [
                "--directory",
                "path/to/mcp2serial",
                "run",
                "mcp2serial"
            ]
        }
    }
}
```

## Troubleshooting

### Common Issues

1. Permission Denied
   - Windows: Run as Administrator
   - Linux/macOS: Add user to dialout group
     ```bash
     sudo usermod -a -G dialout $USER
     ```

2. Port Not Found
   - Check if the device is properly connected
   - Verify port name in device manager
   - Try different USB ports

### Getting Help

If you encounter issues:
1. Check our [FAQ](./faq.md)
2. Open an issue on GitHub
3. Join our community discussions
