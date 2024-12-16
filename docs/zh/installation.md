# MCP2Serial 安装指南

## 环境要求

- Python 3.11 或更高版本
- uv 包管理器
- 串口设备（如Arduino、树莓派Pico等）

## 安装步骤

1. 创建并激活虚拟环境：

```bash
# 进入项目目录
cd mcp2serial

# 使用 uv 创建虚拟环境并安装依赖
uv venv .venv
.venv\Scripts\activate

# 安装依赖
uv pip install -r requirements.txt
```

## 运行服务器

```bash
# 确保在项目根目录下
cd mcp2serial

# 激活虚拟环境（如果尚未激活）
.venv\Scripts\activate

# 运行服务器
uv run src/mcp2serial/server.py
```

## 配置说明

### 串口配置

在 `config.yaml` 文件中配置串口参数：

```yaml
serial:
  port: COM11  # Windows系统示例，Linux下可能是 /dev/ttyUSB0
  baud_rate: 115200  # 波特率
  timeout: 1.0  # 串口超时时间（秒）
  read_timeout: 0.5  # 读取超时时间（秒）
```

如果不指定 `port`，程序会自动搜索可用的串口设备。

### 命令配置

在 `config.yaml` 中添加自定义命令：

```yaml
commands:
  # PWM控制命令示例
  set_pwm:
    command: "PWM {frequency}\n"  # 实际发送的命令格式
    need_parse: false  # 不需要解析响应
    prompts:  # 提示语列表
      - "把PWM调到{value}"
      - "关闭PWM"

  # LED控制命令示例
  led_control:
    command: "LED {state}\n"  # state可以是on/off或其他值
    need_parse: false
    prompts:
      - "打开LED"
      - "关闭LED"
      - "设置LED状态为{state}"

  # 带响应解析的命令示例
  get_sensor:
    command: "GET_SENSOR\n"
    need_parse: true  # 需要解析响应
    prompts:
      - "读取传感器数据"
```

### 响应解析说明

1. 简单响应（`need_parse: false`）：
   - 设备返回 "OK" 开头的消息表示成功
   - 其他响应将被视为错误

2. 需要解析的响应（`need_parse: true`）：
   - 完整响应将在 `result.raw` 字段中返回
   - 可以在应用层进行进一步解析

响应示例：
```python
# 简单响应
{"status": "success"}

# 需要解析的响应
{"status": "success", "result": {"raw": "OK TEMP=25.5,HUMIDITY=60%"}}
```

## 故障排除

1. 串口连接问题：
   - 确认设备已正确连接
   - 检查串口号是否正确
   - 验证波特率设置
   - 检查串口权限（Linux系统）

2. 命令超时：
   - 检查 `timeout` 和 `read_timeout` 设置
   - 确认设备响应时间

## 测试

运行测试用例：

```bash
# 激活虚拟环境（如果尚未激活）
.venv\Scripts\activate

# 运行测试
uv run pytest tests/
```

## 更多信息

详细的API文档和示例请参考 [API文档](../api.md)。
