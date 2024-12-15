# 安装指南

## 系统要求

- Python 3.11 或更高版本
- pip 或 uv 包管理器
- 串口访问权限（某些系统可能需要管理员权限）

## 安装步骤

### 1. 使用 pip 安装

```bash
pip install mcp2serial
```

### 2. 从源码安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/mcp2serial.git
cd mcp2serial

# 以开发模式安装
pip install -e .
```

## 配置说明

### 串口设置

服务会自动检测可用的串口。但您也可以在配置文件中指定特定串口：

1. 在工作目录创建 `config.yaml`：
```yaml
serial:
  port: COM1  # Windows系统
  # port: /dev/ttyUSB0  # Linux系统
  # port: /dev/tty.usbserial-*  # macOS系统
  baud_rate: 115200
```

### Claude 集成

1. 在 Claude 配置中添加以下内容：
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

## 常见问题解决

### 常见问题

1. 权限被拒绝
   - Windows：以管理员身份运行
   - Linux/macOS：将用户添加到 dialout 组
     ```bash
     sudo usermod -a -G dialout $USER
     ```

2. 找不到端口
   - 检查设备是否正确连接
   - 在设备管理器中验证端口名称
   - 尝试不同的 USB 端口

### 获取帮助

如果遇到问题：
1. 查看我们的[常见问题](./faq.md)
2. 在 GitHub 上提交 Issue
3. 加入社区讨论
