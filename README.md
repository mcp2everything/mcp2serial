# MCP2Serial Service

这是一个基于Claude MCP协议的串口通信服务，用于通过串口发送PWM频率控制命令。

## 功能特点

- 自动检测并连接波特率为115200的串口
- 支持发送PWM频率控制命令（频率范围：0-100）
- 符合Claude MCP协议规范
- 提供错误处理和状态反馈

## 安装要求

- Python 3.11+
- pyserial
- mcp

## 运行服务

直接使用 uv run 命令，它会自动完成构建和安装：

```bash
uv run src/mcp2serial/server.py
```

这个命令会：
1. 构建 mcp2serial 包
2. 安装到当前环境
3. 运行服务器

## Claude配置

在Claude的配置文件中添加以下配置：

```json
{
    "mcpServers": {
        "mcp2serial": {
            "command": "uv",
            "args": [
                "--directory",
                "C:\\path\\to\\mcp2serial",
                "run",
                "mcp2serial"
            ]
        }
    }
}
```

注意：请将路径 `C:\\path\\to\\mcp2serial` 替换为实际的项目路径。

## 与Claude对话

服务启动后，你可以直接用自然语言与Claude对话来控制PWM。以下是一些对话示例：

- "请将PWM设置为50%"
- "把PWM调到最大"
- "关闭PWM输出"
- "将PWM频率调整到75%"
- "能帮我把PWM设为25%吗？"

Claude会理解你的意图，自动调用相应的命令来设置PWM频率。你不需要记住具体的命令格式，只需要用自然语言表达你的需求即可。

## API说明

服务提供以下工具：

### set-pwm

设置PWM频率。

参数：
- `frequency`: 整数，范围0-100

返回：
- 成功：`{"status": "success", "message": "OK"}`
- 失败：`{"error": "错误信息"}`

可能的错误信息：
- "Frequency must be between 0 and 100"
- "No available serial port found"
- "Serial communication error: ..."
- "Unexpected response: ..."
