# MCP2Serial Service

[English](README_EN.md) | 简体中文

<div align="center">
    <img src="docs/images/logo.png" alt="MCP2Serial Logo" width="200"/>
</div>

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

## 快速开始

1. 按照 [接线图](docs/images/wiring.png) 连接硬件
2. 使用 Thonny 将 [firmware/src/main.py](firmware/src/main.py) 上传到 Pico
3. 关闭 Thonny（释放串口）
4. 配置并启动服务：
   ```bash
   # 创建虚拟环境并激活
   uv venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate

   # 安装依赖
   uv pip install -e .
   
   # 启动服务
   uv run src/mcp2serial/server.py
   ```

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

![系统架构图](docs/images/architecture.png)
