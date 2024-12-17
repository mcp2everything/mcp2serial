# MCP2Serial: 连接物理世界与AI大模型的桥梁 

[English](README_EN.md) | 简体中文

<div align="center">
    <img src="docs/images/logo.png" alt="MCP2Serial Logo" width="200"/>
    <p>通过自然语言控制硬件，开启物联网新纪元</p>
</div>

## 系统架构

<div align="center">
    <img src="docs/images/stru_chs.png" alt="系统架构图" width="800"/>
    <p>MCP2Serial 系统架构图</p>
</div>

## 工作流程

<div align="center">
    <img src="docs/images/workflow_chs.png" alt="工作流程图" width="800"/>
    <p>MCP2Serial 工作流程图</p>
</div>

## 项目愿景

MCP2Serial 将串口设备接入AI大模型的项目，它通过 Model Context Protocol (MCP) 将物理世界与 AI 大模型无缝连接。最终实现：
- 用自然语言控制你的硬件设备
- AI 实时响应并调整物理参数
- 让你的设备具备理解和执行复杂指令的能力

## 主要特性

- **智能串口通信**
  - 自动检测和配置串口设备 用户也可指定串口号
  - 支持多种波特率（默认 115200）
  - 实时状态监控和错误处理

- **MCP 协议集成**
  - 完整支持 Model Context Protocol
  - 支持资源管理和工具调用
  - 灵活的提示词系统

## 支持的客户端

MCP2Serial 支持所有实现了 MCP 协议的客户端，包括：

| 客户端 | 特性支持 | 说明 |
|--------|----------|------|
| Claude Desktop | 完整支持 | 推荐使用，支持所有 MCP 功能 |
| Continue | 完整支持 | 优秀的开发工具集成 |
| Cline | 资源+工具 | 支持多种 AI 提供商 |
| Zed | 基础支持 | 支持提示词命令 |
| Sourcegraph Cody | 资源支持 | 通过 OpenCTX 集成 |
| Firebase Genkit | 部分支持 | 支持资源列表和工具 |

## 支持的 AI 模型

得益于灵活的客户端支持，MCP2Serial 可以与多种 AI 模型协同工作：

### 云端模型
- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude
- Google Gemini
- AWS Bedrock
- Azure OpenAI
- Google Cloud Vertex AI

### 本地模型
- LM Studio 支持的所有模型
- Ollama 支持的所有模型
- 任何兼容 OpenAI API 的模型

## 快速开始

### 准备
Python3.11 或更高版本
Claude Desktop 或 Cline

### 自动一键安装

#### Windows用户
```bash
# 下载安装脚本
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2serial/main/install.py

# 运行安装脚本
python install.py
```

#### MacOS用户
```bash
# 下载安装脚本
curl -O https://raw.githubusercontent.com/mcp2everything/mcp2serial/main/install_macos.py

# 运行安装脚本
python3 install_macos.py
```

安装脚本会自动完成以下操作：
- ✅ 检查系统环境
- ✅ 安装必要的依赖
- ✅ 创建默认配置文件
- ✅ 配置Claude桌面版（如果已安装）
- ✅ 检查串口设备

### 手动分步安装依赖
```bash
windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
MacOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```
主要依赖uv工具，所以当python和uv以及Claude或Cline安装好后就可以了。

### 基本配置

在你的 MCP 客户端（如 Claude Desktop 或 Cline）配置文件中添加以下内容，注意将路径修改为你的实际安装路径：
注意：如果使用的自动安装那么会自动配置Calude Desktop无需此步。
```json
{
    "mcpServers": {
        "mcp2serial": {
            "command": "uvx",
            "args": ["mcp2serial"]
        }
    }
}
```

<div align="center">
    <img src="docs/images/client_config.png" alt="客户端配置示例" width="600"/>
    <p>在 Claude Desktop 中的配置示例</p>
</div>

<div align="center">
    <img src="docs/images/cline_config.png" alt="Cline配置示例" width="600"/>
    <p>在 Cline 中的配置示例</p>
</div>

> 注意：配置中的路径必须使用完整的绝对路径，并且使用正斜杠（/）或双反斜杠（\\）作为路径分隔符。

配置串口和命令：
```yaml
# config.yaml
serial:
  port: COM11  # 或自动检测
  baud_rate: 115200

commands:
  set_pwm:
    command: "PWM {frequency}\n"
    need_parse: false
    prompts:
      - "把PWM调到{value}"
```
## 配置说明

### 配置文件位置

配置文件（`config.yaml`）可以放在不同位置，程序会按以下顺序查找：

#### 1. 当前工作目录（适合开发测试）
- 路径：`./config.yaml`
- 示例：如果你在 `C:\Projects` 运行程序，它会查找 `C:\Projects\config.yaml`
- 适用场景：开发和测试
- 不需要特殊权限

#### 2. 用户主目录（推荐个人使用）
```bash
# Windows系统
C:\Users\用户名\.mcp2serial\config.yaml

# macOS系统
/Users/用户名/.mcp2serial/config.yaml

# Linux系统
/home/用户名/.mcp2serial/config.yaml
```
- 适用场景：个人配置
- 需要创建 `.mcp2serial` 目录：
  ```bash
  # Windows系统（在命令提示符中）
  mkdir "%USERPROFILE%\.mcp2serial"
  
  # macOS/Linux系统
  mkdir -p ~/.mcp2serial
  ```

#### 3. 系统级配置（适合多用户环境）
```bash
# Windows系统（需要管理员权限）
C:\ProgramData\mcp2serial\config.yaml

# macOS/Linux系统（需要root权限）
/etc/mcp2serial/config.yaml
```
- 适用场景：多用户共享配置
- 创建目录并设置权限：
  ```bash
  # Windows系统（以管理员身份运行）
  mkdir "C:\ProgramData\mcp2serial"
  
  # macOS/Linux系统（以root身份运行）
  sudo mkdir -p /etc/mcp2serial
  sudo chown root:root /etc/mcp2serial
  sudo chmod 755 /etc/mcp2serial
  ```

程序会按照上述顺序查找配置文件，使用找到的第一个有效配置文件。根据你的需求选择合适的位置：
- 开发测试：使用当前目录
- 个人使用：建议使用用户主目录（推荐）
- 多用户环境：使用系统级配置（ProgramData或/etc）

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


### 硬件连接

1. 将你的设备通过USB连接到电脑
2. 打开设备管理器，记下设备的COM端口号
3. 在`config.yaml`中配置正确的端口号和波特率

<div align="center">
    <img src="docs/images/conn
ect.jpg" alt="硬件连接示例" width="600"/>
    <p>硬件连接和COM端口配置</p>
</div>

### 启动客户端Claude 桌面版或Cline

<div align="center">
    <img src="docs/images/pwm.png" alt="Cline Configuration Example" width="600"/>
    <p> Example in Claude</p>
</div>
<div align="center">
    <img src="docs/images/test_output.png" alt="Cline Configuration Example" width="600"/>
    <p>Example in Cline</p>
</div>

### 硬件编程
firmware可以在项目仓库中下载，目前演示的是Pico的micropython代码案例。另存到Pico开发板运行即可。

### 从源码快速开始
```bash
# 通过源码安装：
git clone https://github.com/mcp2everything/mcp2serial.git
cd mcp2serial
uv venv .venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```
1. 安装依赖：
```bash
# 进入项目目录
cd mcp2serial

# 创建虚拟环境并安装依赖
uv venv .venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

2. 配置串口和命令：
```yaml
# config.yaml
serial:
  port: COM11  # 或自动检测
  baud_rate: 115200

commands:
  set_pwm:
    command: "PWM {frequency}\n"
    need_parse: false
    prompts:
      - "把PWM调到{value}"
```

3. 运行服务器：
```bash
# 确保已激活虚拟环境
.venv\Scripts\activate

# 运行服务器
uv run src/mcp2serial/server.py
```

## 文档

- [安装指南](./docs/zh/installation.md)
- [API文档](./docs/zh/api.md)
- [配置说明](./docs/zh/configuration.md)


## 应用场景

1. **智能家居自动化**
   - 通过自然语言控制灯光、风扇等设备
   - AI 根据环境自动调节设备参数

2. **工业自动化**
   - 智能控制生产线设备
   - 实时监控和调整工艺参数

3. **教育和研究**
   - 物联网教学演示
   - 硬件控制实验平台

4. **原型开发**
   - 快速验证硬件控制方案
   - 简化开发流程

## 🚀 项目发展规划

### 第一阶段：协议扩展
- **工业协议支持**
  - MODBUS RTU/TCP
  - OPC UA
  - MQTT
  - CoAP
  - TCP/IP Socket
  
- **硬件接口扩展**
  - I2C
  - SPI
  - CAN
  - 1-Wire
  - GPIO

### 第二阶段：MCP2Anything 平台
- **统一集成平台**
  - 可视化配置界面
  - 一键启用各类协议
  - 实时监控仪表盘
  - 设备管理系统

- **智能功能**
  - 协议自动检测
  - 设备自动发现
  - 参数智能优化
  - 异常预警系统

### 第三阶段：生态系统建设
- **插件市场**
  - 协议插件
  - 设备驱动
  - 自定义功能模块
  - 社区贡献集成

- **云服务集成**
  - 设备云管理
  - 远程控制
  - 数据分析
  - AI 训练平台

### 第四阶段：行业解决方案
- **垂直领域适配**
  - 工业自动化
  - 智能建筑
  - 农业物联网
  - 智慧城市

- **定制化服务**
  - 行业协议适配
  - 专业技术支持
  - 解决方案咨询
  - 培训服务

## 🔮 愿景展望

MCP2Serial 正在开启物联网的新篇章：

- **协议统一**: 通过 MCP2Anything 平台实现全协议支持
- **即插即用**: 一键配置，自动发现，零门槛使用
- **AI 赋能**: 深度集成 AI 能力，实现智能决策
- **开放生态**: 建立活跃的开发者社区和插件市场

## 未来展望

MCP2Serial 正在开启物联网的新篇章：

- **多协议支持**: 计划支持更多通信协议（I2C、SPI等）
- **设备生态**: 建立开放的设备支持生态系统
- **AI 增强**: 集成更多 AI 能力，提供更智能的控制逻辑
- **可视化**: 开发直观的监控和配置界面

## 相关资源

- [MCP 协议规范](https://modelcontextprotocol.io/)
- [项目文档](docs/)
- [示例代码](examples/)
- [常见问题](docs/FAQ.md)

## 参与贡献

我们欢迎各种形式的贡献，无论是新功能、文档改进还是问题报告。查看 [贡献指南](CONTRIBUTING.md) 了解更多信息。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
